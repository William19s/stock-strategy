import yfinance as yf
import pandas as pd

class MAStrategy:
    def __init__(self, symbol, short_window, long_window):
        self.symbol = symbol
        self.short_window = short_window
        self.long_window = long_window
    
    def backtest(self):
        try:
            # 下载股票数据
            stock = yf.download(self.symbol, start='2020-01-01')
            
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
            
            return stock
            
        except Exception as e:
            print(f"发生错误: {e}")
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