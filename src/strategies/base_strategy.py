from abc import ABC, abstractmethod
from typing import Dict, Optional
import pandas as pd
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class BaseStrategy(ABC):
    """策略基类"""
    
    def __init__(self, name: str):
        self.name = name
        self.parameters = {}
        self.position = 0
        self.trades = []
    
    @abstractmethod
    def validate_parameters(self) -> bool:
        """验证参数"""
        pass
    
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """生成交易信号"""
        pass
    
    def calculate_position(self, signal: float, capital: float) -> float:
        """计算持仓"""
        try:
            # 基础仓位计算
            position = signal * self.parameters.get('position_size', 0.1)
            
            # 应用仓位限制
            max_position = self.parameters.get('max_positions', 1.0)
            position = min(max_position, max(-max_position, position))
            
            # 计算实际持仓金额
            position_value = position * capital
            
            return position_value
            
        except Exception as e:
            logger.error(f"仓位计算失败: {str(e)}")
            return 0.0
    
    def add_trade(self, date: str, symbol: str, type: str, 
                  price: float, shares: int, profit: float = 0):
        """记录交易"""
        try:
            self.trades.append({
                'date': date,
                'symbol': symbol,
                'type': type,
                'price': price,
                'shares': shares,
                'profit': profit
            })
        except Exception as e:
            logger.error(f"交易记录失败: {str(e)}")
    
    def get_trades(self) -> pd.DataFrame:
        """获取交易记录"""
        try:
            return pd.DataFrame(self.trades)
        except Exception as e:
            logger.error(f"获取交易记录失败: {str(e)}")
            return pd.DataFrame()
    
    def reset(self):
        """重置策略状态"""
        try:
            self.position = 0
            self.trades = []
        except Exception as e:
            logger.error(f"策略重置失败: {str(e)}") 