from abc import ABC, abstractmethod
import pandas as pd
from typing import Optional
from ..indicators.technical import TechnicalIndicators
from ..data.data_loader import DataLoader

class BaseStrategy(ABC):
    """策略基类"""
    
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.data_loader = DataLoader()
        self.tech_indicators = TechnicalIndicators()
        self.name = "BaseStrategy"
        
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """生成交易信号"""
        pass
    
    @abstractmethod
    def validate_parameters(self) -> bool:
        """验证策略参数"""
        pass
    
    def get_data(self, start_date: str = '2020-01-01') -> Optional[pd.DataFrame]:
        """获取数据"""
        return self.data_loader.get_stock_data(self.symbol, start_date)
    
    def calculate_returns(self, data: pd.DataFrame) -> pd.DataFrame:
        """计算收益"""
        data['Returns'] = data['Close'].pct_change()
        data['Strategy_Returns'] = data['Signal'].shift(1) * data['Returns']
        data['Cumulative_Returns'] = (1 + data['Returns']).cumprod()
        data['Strategy_Cumulative_Returns'] = (1 + data['Strategy_Returns']).cumprod()
        return data
    
    def run_strategy(self, start_date: str = '2020-01-01') -> Optional[pd.DataFrame]:
        """运行策略"""
        if not self.validate_parameters():
            return None
            
        data = self.get_data(start_date)
        if data is None:
            return None
            
        data = self.generate_signals(data)
        return self.calculate_returns(data) 