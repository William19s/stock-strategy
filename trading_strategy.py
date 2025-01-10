import baostock as bs
import pandas as pd

class MAStrategy:
    def __init__(self, symbol, short_window, long_window):
        self.symbol = symbol  # 例如："sh.600000" 浦发银行
        self.short_window = short_window
        self.long_window = long_window
    
    def backtest(self):
        try:
            # 登录系统
            lg = bs.login()
            if lg.error_code != '0':
                print(f'登录失败: {lg.error_msg}')
                return None
            
            # 获取股票数据
            rs = bs.query_history_k_data_plus(
                self.symbol,
                "date,close",
                start_date='2020-01-01',
                frequency="d",
                adjustflag="3"  # 复权类型：3表示后复权
            )
            
            if rs.error_code != '0':
                print(f'获取数据失败: {rs.error_msg}')
                bs.logout()
                return None
            
            # 转换数据格式
            data_list = []
            while (rs.error_code == '0') & rs.next():
                data_list.append(rs.get_row_data())
            
            if not data_list:
                print('未获取到任何数据')
                bs.logout()
                return None
            
            # 创建DataFrame
            stock = pd.DataFrame(data_list, columns=['date', 'Close'])
            stock['Close'] = stock['Close'].astype(float)
            stock.set_index('date', inplace=True)
            
            # 计算移动平均线
            stock['SMA_short'] = stock['Close'].rolling(window=self.short_window).mean()
            stock['SMA_long'] = stock['Close'].rolling(window=self.long_window).mean()
            
            # 生成交易信号
            stock['Signal'] = 0
            stock.loc[stock['SMA_short'] > stock['SMA_long'], 'Signal'] = 1
            
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