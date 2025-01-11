import pandas as pd
import numpy as np
from typing import Dict
from .base_strategy import BaseStrategy
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class VolumeBreakoutStrategy(BaseStrategy):
    """量价突破策略"""
    
    def __init__(self):
        super().__init__("量价突破策略")
        self.parameters = {
            'price_ma_period': 20,     # 价格均线周期
            'volume_ma_period': 20,    # 成交量均线周期
            'breakout_std': 2.0,       # 突破标准差
            'volume_ratio': 2.0,       # 放量倍数
            'lookback_period': 20,     # 回看周期
            'position_size': 0.1       # 仓位比例
        }
    
    def validate_parameters(self) -> bool:
        """验证参数"""
        try:
            if not all(isinstance(v, (int, float)) for v in self.parameters.values()):
                logger.error("参数类型错误")
                return False
            if any(v <= 0 for v in self.parameters.values()):
                logger.error("参数必须为正数")
                return False
            return True
        except Exception as e:
            logger.error(f"参数验证失败: {str(e)}")
            return False
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """生成交易信号"""
        try:
            # 计算技术指标
            price_ma = data['close'].rolling(window=self.parameters['price_ma_period']).mean()
            volume_ma = data['volume'].rolling(window=self.parameters['volume_ma_period']).mean()
            
            # 计算价格通道
            price_std = data['close'].rolling(window=self.parameters['lookback_period']).std()
            upper_band = price_ma + self.parameters['breakout_std'] * price_std
            lower_band = price_ma - self.parameters['breakout_std'] * price_std
            
            # 计算成交量比率
            volume_ratio = data['volume'] / volume_ma
            
            # 生成信号
            data['signal'] = 0
            
            # 上突破信号
            long_condition = (
                (data['close'] > upper_band) & 
                (volume_ratio > self.parameters['volume_ratio']) &
                (data['close'] > price_ma)
            )
            data.loc[long_condition, 'signal'] = 1
            
            # 下突破信号
            short_condition = (
                (data['close'] < lower_band) & 
                (volume_ratio > self.parameters['volume_ratio']) &
                (data['close'] < price_ma)
            )
            data.loc[short_condition, 'signal'] = -1
            
            return data
            
        except Exception as e:
            logger.error(f"信号生成失败: {str(e)}")
            return pd.DataFrame() 