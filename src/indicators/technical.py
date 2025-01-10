import pandas as pd
import numpy as np

class TechnicalIndicators:
    """技术指标计算类"""
    
    @staticmethod
    def calculate_ma(data: pd.Series, window: int) -> pd.Series:
        """计算移动平均线"""
        return data.rolling(window=window).mean()
    
    @staticmethod
    def calculate_macd(data: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> tuple:
        """计算MACD指标"""
        exp1 = data.ewm(span=fast, adjust=False).mean()
        exp2 = data.ewm(span=slow, adjust=False).mean()
        macd = exp1 - exp2
        signal_line = macd.ewm(span=signal, adjust=False).mean()
        hist = macd - signal_line
        return macd, signal_line, hist
    
    @staticmethod
    def calculate_rsi(data: pd.Series, period: int = 14) -> pd.Series:
        """计算RSI指标"""
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    @staticmethod
    def calculate_kdj(data: pd.DataFrame, n: int = 9, m1: int = 3, m2: int = 3) -> tuple:
        """计算KDJ指标"""
        low_min = data['Low'].rolling(window=n).min()
        high_max = data['High'].rolling(window=n).max()
        rsv = (data['Close'] - low_min) / (high_max - low_min) * 100
        k = rsv.rolling(window=m1).mean()
        d = k.rolling(window=m2).mean()
        j = 3 * k - 2 * d
        return k, d, j
    
    @staticmethod
    def calculate_volume_ma(volume: pd.Series, window: int = 5) -> pd.Series:
        """计算成交量移动平均"""
        return volume.rolling(window=window).mean() 