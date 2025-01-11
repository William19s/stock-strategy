import pandas as pd
import numpy as np
from typing import Tuple
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class VolatilityIndicators:
    """波动率指标"""
    
    @staticmethod
    def calculate_atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
        """计算ATR"""
        try:
            tr1 = high - low
            tr2 = abs(high - close.shift())
            tr3 = abs(low - close.shift())
            tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            return tr.rolling(window=period).mean()
        except Exception as e:
            logger.error(f"ATR计算失败: {str(e)}")
            return pd.Series()
    
    @staticmethod
    def calculate_bollinger_bands(close: pd.Series, period: int = 20, std_dev: float = 2.0) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """计算布林带"""
        try:
            middle = close.rolling(window=period).mean()
            std = close.rolling(window=period).std()
            upper = middle + std_dev * std
            lower = middle - std_dev * std
            return upper, middle, lower
        except Exception as e:
            logger.error(f"布林带计算失败: {str(e)}")
            return pd.Series(), pd.Series(), pd.Series() 