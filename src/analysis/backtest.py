import pandas as pd
from typing import Optional, Dict
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class BacktestEngine:
    """回测引擎"""
    
    def __init__(self, strategy, initial_capital: float = 100000.0):
        self.strategy = strategy
        self.initial_capital = initial_capital
        self.positions = {}
        self.cash = initial_capital
        
    def run(self, data: pd.DataFrame) -> Dict:
        """运行回测"""
        try:
            # 生成信号
            results = self.strategy.run_strategy()
            if results is None:
                return None
            
            # 计算交易统计
            stats = self._calculate_statistics(results)
            
            return {
                'results': results,
                'stats': stats
            }
            
        except Exception as e:
            logger.error(f"Backtest error: {str(e)}")
            return None
    
    def _calculate_statistics(self, results: pd.DataFrame) -> Dict:
        """计算回测统计数据"""
        stats = {}
        
        # 计算总收益
        total_return = (
            results['Strategy_Cumulative_Returns'].iloc[-1] - 1
        ) * 100
        
        # 计算年化收益
        days = len(results)
        annual_return = (
            (1 + total_return/100) ** (252/days) - 1
        ) * 100
        
        # 计算最大回撤
        cummax = results['Strategy_Cumulative_Returns'].cummax()
        drawdown = (cummax - results['Strategy_Cumulative_Returns']) / cummax
        max_drawdown = drawdown.max() * 100
        
        # 计算夏普比率
        daily_returns = results['Strategy_Returns']
        sharpe_ratio = (
            daily_returns.mean() / daily_returns.std()
        ) * (252 ** 0.5)
        
        stats['total_return'] = total_return
        stats['annual_return'] = annual_return
        stats['max_drawdown'] = max_drawdown
        stats['sharpe_ratio'] = sharpe_ratio
        stats['win_rate'] = (results['Strategy_Returns'] > 0).mean() * 100
        
        return stats 