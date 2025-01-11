import pandas as pd
import numpy as np
from typing import Tuple, Optional
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class MomentumIndicators:
    """动量指标"""
    
    @staticmethod
    def calculate_rsi(close: pd.Series, period: int = 14) -> pd.Series:
        """计算RSI"""
        try:
            # 1. 向量化运算
            delta = close.diff()
            # 2. 使用numpy代替pandas where
            gains = np.where(delta > 0, delta, 0)
            losses = np.where(delta < 0, -delta, 0)
            
            # 3. 使用expanding窗口避免数据丢失
            avg_gains = pd.Series(gains).ewm(alpha=1/period, adjust=False).mean()
            avg_losses = pd.Series(losses).ewm(alpha=1/period, adjust=False).mean()
            
            # 4. 避免除零错误
            rs = np.divide(avg_gains, avg_losses, out=np.zeros_like(avg_gains), where=avg_losses!=0)
            return 100 - (100 / (1 + rs))
            
        except Exception as e:
            logger.error(f"RSI计算失败: {str(e)}")
            return pd.Series()
    
    @staticmethod
    def calculate_macd(
        close: pd.Series,
        fast_period: int = 12,
        slow_period: int = 26,
        signal_period: int = 9
    ) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """计算MACD"""
        try:
            exp1 = close.ewm(span=fast_period, adjust=False).mean()
            exp2 = close.ewm(span=slow_period, adjust=False).mean()
            macd = exp1 - exp2
            signal = macd.ewm(span=signal_period, adjust=False).mean()
            hist = macd - signal
            return macd, signal, hist
        except Exception as e:
            logger.error(f"MACD计算失败: {str(e)}")
            return pd.Series(), pd.Series(), pd.Series()
    
    @staticmethod
    def calculate_kdj(
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        n: int = 9,
        m1: int = 3,
        m2: int = 3
    ) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """计算KDJ"""
        try:
            rsv = (close - low.rolling(n).min()) / (
                high.rolling(n).max() - low.rolling(n).min()
            ) * 100
            k = pd.DataFrame(rsv).ewm(com=m1-1).mean()
            d = k.ewm(com=m2-1).mean()
            j = 3 * k - 2 * d
            return k[0], d[0], j[0]
        except Exception as e:
            logger.error(f"KDJ计算失败: {str(e)}")
            return pd.Series(), pd.Series(), pd.Series() 