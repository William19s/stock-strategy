import pandas as pd
import numpy as np
from typing import Dict
from .base_strategy import BaseStrategy
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class FactorStrategy(BaseStrategy):
    """多因子策略"""
    
    def __init__(self):
        super().__init__("多因子策略")
        self.parameters = {
            'momentum_period': 20,    # 动量因子周期
            'volatility_period': 20,  # 波动率因子周期
            'volume_period': 20,      # 成交量因子周期
            'position_size': 0.1      # 仓位比例
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
            # 计算因子
            # 1. 动量因子
            data['momentum'] = data['close'].pct_change(self.parameters['momentum_period'])
            
            # 2. 波动率因子
            data['volatility'] = data['close'].pct_change().rolling(
                self.parameters['volatility_period']
            ).std()
            
            # 3. 成交量因子
            data['volume_factor'] = data['volume'].rolling(
                self.parameters['volume_period']
            ).mean()
            
            # 生成信号
            data['signal'] = 0
            
            # 综合因子得分
            data['factor_score'] = (
                data['momentum'].rank(pct=True) * 0.4 +
                (1 - data['volatility'].rank(pct=True)) * 0.3 +
                data['volume_factor'].rank(pct=True) * 0.3
            )
            
            # 根据因子得分生成信号
            data.loc[data['factor_score'] > 0.8, 'signal'] = 1
            data.loc[data['factor_score'] < 0.2, 'signal'] = -1
            
            return data
            
        except Exception as e:
            logger.error(f"信号生成失败: {str(e)}")
            return pd.DataFrame() 