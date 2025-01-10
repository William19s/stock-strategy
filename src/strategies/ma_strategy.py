from .base_strategy import BaseStrategy
from ..indicators.technical import TechnicalIndicators

class MAStrategy(BaseStrategy):
    def __init__(self, symbol, short_window, long_window):
        super().__init__(symbol)
        self.short_window = short_window
        self.long_window = long_window
        self.tech_indicators = TechnicalIndicators()
    
    def generate_signals(self, data):
        # 移动原 trading_strategy.py 中的信号生成逻辑
        signals = self.tech_indicators.calculate_ma_signals(
            data, self.short_window, self.long_window
        )
        return signals 