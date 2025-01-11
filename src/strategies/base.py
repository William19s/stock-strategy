from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, Any

class BaseStrategy(ABC):
    """策略基类"""
    
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.params: Dict[str, Any] = {}
    
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """生成交易信号"""
        pass
    
    @abstractmethod
    def validate_parameters(self) -> bool:
        """验证策略参数"""
        pass
    
    def run_strategy(self, data: pd.DataFrame) -> pd.DataFrame:
        """运行策略"""
        if not self.validate_parameters():
            raise ValueError("策略参数无效")
        
        signals = self.generate_signals(data)
        return pd.DataFrame({
            'close': data['close'],
            'signal': signals
        }) 