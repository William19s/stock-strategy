import pandas as pd
import numpy as np
from typing import Dict, Optional
from .base_strategy import BaseStrategy
from ..indicators.momentum import MomentumIndicators
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class MeanReversionStrategy(BaseStrategy):
    """均值回归策略"""
    
    def __init__(self, name: str = "均值回归"):
        super().__init__(name)
        self.momentum_indicators = MomentumIndicators()
        self.parameters = {
            'ma_period': 20,        # 均线周期
            'std_dev': 2.0,         # 标准差倍数
            'rsi_period': 14,       # RSI周期
            'rsi_upper': 70,        # RSI超买阈值
            'rsi_lower': 30,        # RSI超卖阈值
            'position_size': 0.1    # 仓位比例
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
            data['ma'] = data['close'].rolling(
                window=self.parameters['ma_period']
            ).mean()
            data['std'] = data['close'].rolling(
                window=self.parameters['ma_period']
            ).std()
            data['upper_band'] = data['ma'] + self.parameters['std_dev'] * data['std']
            data['lower_band'] = data['ma'] - self.parameters['std_dev'] * data['std']
            
            data['rsi'] = self.momentum_indicators.calculate_rsi(
                data['close'],
                self.parameters['rsi_period']
            )
            
            # 生成信号
            data['signal'] = 0
            # 超卖做多
            data.loc[
                (data['close'] < data['lower_band']) & 
                (data['rsi'] < self.parameters['rsi_lower']),
                'signal'
            ] = 1
            # 超买做空
            data.loc[
                (data['close'] > data['upper_band']) & 
                (data['rsi'] > self.parameters['rsi_upper']),
                'signal'
            ] = -1
            
            # 计算持仓规模
            data['position_size'] = data['signal'] * self.parameters['position_size']
            
            return data
            
        except Exception as e:
            logger.error(f"信号生成失败: {str(e)}")
            return pd.DataFrame() 