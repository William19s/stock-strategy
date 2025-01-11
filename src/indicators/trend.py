import pandas as pd
import numpy as np
from typing import Tuple, Optional
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class TrendIndicators:
    """趋势指标"""
    
    @staticmethod
    def calculate_adx(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """计算ADX指标"""
        try:
            # 计算方向移动
            up_move = high - high.shift(1)
            down_move = low.shift(1) - low
            
            plus_dm = pd.Series(0, index=up_move.index)
            plus_dm[(up_move > down_move) & (up_move > 0)] = up_move
            
            minus_dm = pd.Series(0, index=down_move.index)
            minus_dm[(down_move > up_move) & (down_move > 0)] = down_move
            
            # 计算TR
            tr1 = high - low
            tr2 = abs(high - close.shift(1))
            tr3 = abs(low - close.shift(1))
            tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            
            # 计算方向指标
            plus_di = 100 * plus_dm.rolling(period).mean() / tr.rolling(period).mean()
            minus_di = 100 * minus_dm.rolling(period).mean() / tr.rolling(period).mean()
            
            # 计算ADX
            dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
            adx = dx.rolling(period).mean()
            
            return adx, plus_di, minus_di
            
        except Exception as e:
            logger.error(f"ADX计算失败: {str(e)}")
            return pd.Series(), pd.Series(), pd.Series()
    
    @staticmethod
    def calculate_supertrend(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 10, multiplier: float = 3.0) -> Tuple[pd.Series, pd.Series]:
        """计算SuperTrend指标"""
        try:
            # 计算ATR
            tr1 = high - low
            tr2 = abs(high - close.shift(1))
            tr3 = abs(low - close.shift(1))
            tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            atr = tr.rolling(period).mean()
            
            # 计算基础上下轨
            basic_upper = (high + low) / 2 + multiplier * atr
            basic_lower = (high + low) / 2 - multiplier * atr
            
            # 计算最终上下轨
            final_upper = pd.Series(index=close.index)
            final_lower = pd.Series(index=close.index)
            
            for i in range(len(close)):
                if i == 0:
                    final_upper.iloc[i] = basic_upper.iloc[i]
                    final_lower.iloc[i] = basic_lower.iloc[i]
                else:
                    final_upper.iloc[i] = (
                        basic_upper.iloc[i] 
                        if (basic_upper.iloc[i] < final_upper.iloc[i-1] or close.iloc[i-1] > final_upper.iloc[i-1])
                        else final_upper.iloc[i-1]
                    )
                    final_lower.iloc[i] = (
                        basic_lower.iloc[i]
                        if (basic_lower.iloc[i] > final_lower.iloc[i-1] or close.iloc[i-1] < final_lower.iloc[i-1])
                        else final_lower.iloc[i-1]
                    )
            
            # 计算SuperTrend
            supertrend = pd.Series(index=close.index)
            for i in range(len(close)):
                if i == 0:
                    supertrend.iloc[i] = final_upper.iloc[i]
                else:
                    supertrend.iloc[i] = (
                        final_upper.iloc[i]
                        if (supertrend.iloc[i-1] == final_upper.iloc[i-1] and close.iloc[i] <= final_upper.iloc[i])
                        else (final_lower.iloc[i]
                             if (supertrend.iloc[i-1] == final_upper.iloc[i-1] and close.iloc[i] > final_upper.iloc[i])
                             else (final_lower.iloc[i]
                                  if (supertrend.iloc[i-1] == final_lower.iloc[i-1] and close.iloc[i] >= final_lower.iloc[i])
                                  else final_upper.iloc[i]))
                    )
            
            return supertrend, pd.Series(close > supertrend).astype(int)
            
        except Exception as e:
            logger.error(f"SuperTrend计算失败: {str(e)}")
            return pd.Series(), pd.Series() 