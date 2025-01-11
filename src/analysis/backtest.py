import pandas as pd
import numpy as np
from typing import Dict, Optional
from ..strategies.base import BaseStrategy
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class BacktestEngine:
    """回测引擎"""
    
    def __init__(self, strategy: BaseStrategy, initial_capital: float = 1000000):
        self.strategy = strategy
        self.initial_capital = initial_capital
        self.positions = pd.Series()
        self.portfolio = pd.Series()
    
    def run(self, data: Optional[pd.DataFrame] = None) -> Dict:
        """运行回测"""
        try:
            # 运行策略获取信号
            results = self.strategy.run_strategy(data)
            signals = results['signal']
            
            # 计算持仓
            self.positions = signals.shift(1).fillna(0)
            
            # 计算收益
            returns = data['close'].pct_change()
            strategy_returns = self.positions * returns
            
            # 计算资金曲线
            self.portfolio = (1 + strategy_returns).cumprod() * self.initial_capital
            
            return {
                'signals': signals,
                'positions': self.positions,
                'returns': strategy_returns,
                'portfolio': self.portfolio
            }
            
        except Exception as e:
            logger.error(f"回测执行失败: {str(e)}")
            raise 