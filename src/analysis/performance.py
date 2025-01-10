import pandas as pd
import numpy as np
from typing import Dict, Optional
import matplotlib.pyplot as plt

class PerformanceAnalyzer:
    """性能分析器"""
    
    def __init__(self, results: pd.DataFrame):
        self.results = results
    
    def calculate_metrics(self) -> Dict:
        """计算性能指标"""
        metrics = {}
        
        # 收益指标
        metrics['total_trades'] = len(self.results[self.results['Signal'].diff() != 0])
        metrics['win_rate'] = (self.results['Strategy_Returns'] > 0).mean() * 100
        
        # 风险指标
        metrics['max_drawdown'] = self._calculate_max_drawdown()
        metrics['volatility'] = self.results['Strategy_Returns'].std() * (252 ** 0.5) * 100
        metrics['sharpe_ratio'] = self._calculate_sharpe_ratio()
        
        return metrics
    
    def plot_performance(self) -> plt.Figure:
        """绘制性能图表"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))
        
        # 绘制价格和信号
        self._plot_price_and_signals(ax1)
        
        # 绘制收益对比
        self._plot_returns_comparison(ax2)
        
        plt.tight_layout()
        return fig
    
    def _calculate_max_drawdown(self) -> float:
        """计算最大回撤"""
        cumulative_returns = self.results['Strategy_Cumulative_Returns']
        rolling_max = cumulative_returns.cummax()
        drawdown = (rolling_max - cumulative_returns) / rolling_max
        return drawdown.max() * 100
    
    def _calculate_sharpe_ratio(self) -> float:
        """计算夏普比率"""
        returns = self.results['Strategy_Returns']
        return (returns.mean() / returns.std()) * (252 ** 0.5) 