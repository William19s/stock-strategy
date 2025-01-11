import numpy as np
import pandas as pd
import talib
from typing import Tuple, Optional
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class TechnicalIndicators:
    """技术分析指标"""
    
    @staticmethod
    def calculate_ma(close: pd.Series, periods: list = [5, 10, 20, 60]) -> pd.DataFrame:
        """计算多周期移动平均"""
        try:
            ma_dict = {}
            for period in periods:
                ma_dict[f'MA{period}'] = talib.MA(close, timeperiod=period)
            return pd.DataFrame(ma_dict)
        except Exception as e:
            logger.error(f"MA计算失败: {str(e)}")
            return pd.DataFrame()
    
    @staticmethod
    def calculate_bollinger_bands(
        close: pd.Series,
        period: int = 20,
        std_dev: float = 2.0
    ) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """计算布林带"""
        try:
            upper, middle, lower = talib.BBANDS(
                close,
                timeperiod=period,
                nbdevup=std_dev,
                nbdevdn=std_dev
            )
            return upper, middle, lower
        except Exception as e:
            logger.error(f"布林带计算失败: {str(e)}")
            return pd.Series(), pd.Series(), pd.Series()
    
    @staticmethod
    def calculate_volume_indicators(
        close: pd.Series,
        volume: pd.Series,
        high: pd.Series,
        low: pd.Series
    ) -> pd.DataFrame:
        """计算成交量指标"""
        try:
            indicators = {}
            # OBV - On Balance Volume
            indicators['OBV'] = talib.OBV(close, volume)
            # AD - Chaikin A/D Line
            indicators['AD'] = talib.AD(high, low, close, volume)
            # CMF - Chaikin Money Flow
            indicators['CMF'] = talib.ADOSC(high, low, close, volume)
            return pd.DataFrame(indicators)
        except Exception as e:
            logger.error(f"成交量指标计算失败: {str(e)}")
            return pd.DataFrame()
    
    @staticmethod
    def calculate_trend_indicators(
        close: pd.Series,
        high: pd.Series,
        low: pd.Series
    ) -> pd.DataFrame:
        """计算趋势指标"""
        try:
            indicators = {}
            # ADX - Average Directional Index
            indicators['ADX'] = talib.ADX(high, low, close, timeperiod=14)
            # CCI - Commodity Channel Index
            indicators['CCI'] = talib.CCI(high, low, close, timeperiod=14)
            # DX - Directional Movement Index
            indicators['DX'] = talib.DX(high, low, close, timeperiod=14)
            return pd.DataFrame(indicators)
        except Exception as e:
            logger.error(f"趋势指标计算失败: {str(e)}")
            return pd.DataFrame() 