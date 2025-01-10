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