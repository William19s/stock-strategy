import baostock as bs
import pandas as pd

class MAStrategy:
    def __init__(self, symbol, short_window, long_window):
        # 统一处理股票代码格式
        if symbol.isdigit():
            # 上海证券交易所
            if symbol.startswith('6'):
                self.symbol = f"sh.{symbol}"
            # 深圳证券交易所
            else:
                self.symbol = f"sz.{symbol}"
        else:
            self.symbol = symbol
            
        self.short_window = short_window
        self.long_window = long_window
        
    def get_stock_name(self):
        try:
            lg = bs.login()
            rs = bs.query_stock_basic(code=self.symbol)
            if rs.error_code == '0' and rs.next():
                stock_info = rs.get_row_data()
                name = stock_info[1]  # 股票名称在第二列
                bs.logout()
                return name
            bs.logout()
            return None
        except:
            bs.logout()
            return None
    
    def get_stock_basic_info(self):
        try:
            lg = bs.login()
            rs = bs.query_stock_basic(code=self.symbol)
            if rs.error_code == '0' and rs.next():
                stock_info = rs.get_row_data()
                name = stock_info[1]  # 股票名称
                market_cap = float(stock_info[11]) if stock_info[11] else 0  # 总市值
                bs.logout()
                return {'name': name, 'market_cap': market_cap}
            bs.logout()
            return None
        except:
            bs.logout()
            return None
    
    def backtest(self):
        try:
            # 登录系统
            lg = bs.login()
            if lg.error_code != '0':
                print(f'登录失败: {lg.error_msg}')
                return None
            
            print(f"正在获取股票数据: {self.symbol}")  # 添加调试信息
            
            # 获取股票数据
            rs = bs.query_history_k_data_plus(
                self.symbol,
                "date,close,volume",
                start_date='2020-01-01',
                frequency="d",
                adjustflag="3"  # 复权类型：3表示后复权
            )
            
            if rs.error_code != '0':
                print(f'获取数据失败: {rs.error_msg}, 错误代码: {rs.error_code}')
                bs.logout()
                return None
            
            # 转换数据格式
            data_list = []
            while (rs.error_code == '0') & rs.next():
                data_list.append(rs.get_row_data())
            
            if not data_list:
                print(f'未获取到数据，可能原因：\n1. 股票代码格式错误\n2. 股票未上市或已退市\n3. 数据源暂不支持')
                bs.logout()
                return None
            
            # 创建DataFrame
            stock = pd.DataFrame(data_list, columns=['date', 'Close', 'volume'])
            stock['Close'] = stock['Close'].astype(float)
            stock['volume'] = stock['volume'].astype(float)
            stock.set_index('date', inplace=True)
            
            # 计算移动平均线
            stock['SMA_short'] = stock['Close'].rolling(window=self.short_window).mean()
            stock['SMA_long'] = stock['Close'].rolling(window=self.long_window).mean()
            
            # 添加成交量条件
            stock['Volume'] = stock['volume'].astype(float)
            stock['Volume_MA5'] = stock['Volume'].rolling(window=5).mean()
            volume_condition = stock['Volume'] > stock['Volume_MA5']
            
            # 获取市值信息
            basic_info = self.get_stock_basic_info()
            if basic_info:
                market_cap = basic_info['market_cap']
                market_cap_condition = 80 <= market_cap <= 500
            else:
                market_cap_condition = True  # 如果无法获取市值信息，则忽略此条件
            
            # 计算技术指标
            # MACD
            exp1 = stock['Close'].ewm(span=12, adjust=False).mean()
            exp2 = stock['Close'].ewm(span=26, adjust=False).mean()
            stock['MACD'] = exp1 - exp2
            stock['Signal_Line'] = stock['MACD'].ewm(span=9, adjust=False).mean()
            stock['MACD_Hist'] = stock['MACD'] - stock['Signal_Line']
            
            # RSI
            delta = stock['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            stock['RSI'] = 100 - (100 / (1 + rs))
            
            # KDJ
            low_min = stock['Close'].rolling(window=9).min()
            high_max = stock['Close'].rolling(window=9).max()
            stock['RSV'] = (stock['Close'] - low_min) / (high_max - low_min) * 100
            stock['K'] = stock['RSV'].rolling(window=3).mean()
            stock['D'] = stock['K'].rolling(window=3).mean()
            stock['J'] = 3 * stock['K'] - 2 * stock['D']
            
            # 生成交易信号（综合多个指标）
            stock['Signal'] = 0
            stock.loc[
                (stock['SMA_short'] > stock['SMA_long']) &  # 均线条件
                (stock['MACD'] > stock['Signal_Line']) &    # MACD金叉
                (stock['RSI'] > 30) & (stock['RSI'] < 70) & # RSI不过度超买超卖
                (stock['K'] > stock['D']) &                 # KDJ金叉
                (stock['Close'] > 5) &                      # 股价条件
                volume_condition &                          # 成交量条件
                market_cap_condition,                       # 市值条件
                'Signal'
            ] = 1
            
            # 添加卖出信号（可选）
            stock.loc[
                (stock['SMA_short'] < stock['SMA_long']) |  # 均线死叉
                (stock['MACD'] < stock['Signal_Line']) |    # MACD死叉
                (stock['RSI'] > 80) |                       # RSI超买
                (stock['K'] < stock['D']),                  # KDJ死叉
                'Signal'
            ] = 0
            
            # 计算每日收益
            stock['Returns'] = stock['Close'].pct_change()
            stock['Strategy_Returns'] = stock['Signal'].shift(1) * stock['Returns']
            
            # 计算累计收益
            stock['Cumulative_Returns'] = (1 + stock['Returns']).cumprod()
            stock['Strategy_Cumulative_Returns'] = (1 + stock['Strategy_Returns']).cumprod()
            
            # 退出系统
            bs.logout()
            
            return stock
            
        except Exception as e:
            print(f"发生错误: {e}")
            bs.logout()
            return None 
    
    def add_indicators(self, df):
        # RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # MACD
        exp1 = df['Close'].ewm(span=12, adjust=False).mean()
        exp2 = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = exp1 - exp2
        df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
        
        return df 