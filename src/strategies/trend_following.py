import pandas as pd
import numpy as np
from typing import Dict
from .base_strategy import BaseStrategy
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class TrendFollowingStrategy(BaseStrategy):
    """趋势跟踪策略"""
    
    def __init__(self):
        super().__init__("趋势跟踪策略")
        self.parameters = {
            'fast_period': 10,
            'slow_period': 30,
            'atr_period': 14,
            'atr_multiplier': 2.0,
            'position_size': 0.1,
            'max_positions': 1.0,
            'stop_loss': 0.05,
            'take_profit': 0.15
        }
    
    def validate_parameters(self) -> bool:
        """验证参数"""
        try:
            # 验证周期参数
            if self.parameters['fast_period'] >= self.parameters['slow_period']:
                logger.error("快速周期必须小于慢速周期")
                return False
            
            # 验证ATR参数
            if self.parameters['atr_period'] < 1:
                logger.error("ATR周期必须大于0")
                return False
            
            # 验证仓位参数
            if not 0 < self.parameters['position_size'] <= 1:
                logger.error("仓位比例必须在0-1之间")
                return False
            
            # 验证止损止盈
            if self.parameters['stop_loss'] <= 0:
                logger.error("止损比例必须大于0")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"参数验证失败: {str(e)}")
            return False
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """生成交易信号"""
        try:
            # 计算快速均线
            data['ma_fast'] = data['close'].rolling(
                window=self.parameters['fast_period']
            ).mean()
            
            # 计算慢速均线
            data['ma_slow'] = data['close'].rolling(
                window=self.parameters['slow_period']
            ).mean()
            
            # 计算ATR
            data['tr'] = np.maximum(
                data['high'] - data['low'],
                np.maximum(
                    abs(data['high'] - data['close'].shift(1)),
                    abs(data['low'] - data['close'].shift(1))
                )
            )
            data['atr'] = data['tr'].rolling(
                window=self.parameters['atr_period']
            ).mean()
            
            # 生成信号
            data['signal'] = 0
            data.loc[data['ma_fast'] > data['ma_slow'], 'signal'] = 1
            data.loc[data['ma_fast'] < data['ma_slow'], 'signal'] = -1
            
            return data
            
        except Exception as e:
            logger.error(f"信号生成失败: {str(e)}")
            return pd.DataFrame() 