import pandas as pd
from typing import Dict
from .base import BaseStrategy
from ..indicators.trend import calculate_ma

class MAStrategy(BaseStrategy):
    """均线交叉策略"""
    
    def __init__(self, symbol: str, short_window: int = 20, long_window: int = 60):
        super().__init__(symbol)
        self.params = {
            'short_window': short_window,
            'long_window': long_window
        }
    
    def validate_parameters(self) -> bool:
        """验证策略参数"""
        if not isinstance(self.params['short_window'], int):
            return False
        if not isinstance(self.params['long_window'], int):
            return False
        if self.params['short_window'] >= self.params['long_window']:
            return False
        return True
    
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """生成交易信号"""
        short_ma = calculate_ma(data['close'], self.params['short_window'])
        long_ma = calculate_ma(data['close'], self.params['long_window'])
        
        signals = pd.Series(0, index=data.index)
        signals[short_ma > long_ma] = 1
        signals[short_ma < long_ma] = -1
        
        return signals 