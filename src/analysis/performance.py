import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import matplotlib.pyplot as plt
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class PerformanceAnalyzer:
    """策略性能分析"""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.returns = None
        self.cum_returns = None
        self.annual_return = None
        self.max_drawdown = None
        self.sharpe_ratio = None
        self.win_rate = None
        
    def calculate_metrics(self) -> Dict:
        """计算性能指标"""
        try:
            # 计算收益率
            self.returns = self.data['close'].pct_change()
            self.cum_returns = (1 + self.returns).cumprod()
            
            # 年化收益率
            days = len(self.returns)
            self.annual_return = (self.cum_returns.iloc[-1] ** (252/days)) - 1
            
            # 最大回撤
            rolling_max = self.cum_returns.expanding().max()
            drawdowns = self.cum_returns / rolling_max - 1
            self.max_drawdown = drawdowns.min()
            
            # 夏普比率
            risk_free_rate = 0.03  # 假设无风险利率3%
            excess_returns = self.returns - (risk_free_rate/252)
            self.sharpe_ratio = np.sqrt(252) * excess_returns.mean() / excess_returns.std()
            
            # 胜率
            winning_days = (self.returns > 0).sum()
            total_days = len(self.returns.dropna())
            self.win_rate = winning_days / total_days if total_days > 0 else 0
            
            return {
                'annual_return': self.annual_return * 100,
                'max_drawdown': self.max_drawdown * 100,
                'sharpe_ratio': self.sharpe_ratio,
                'win_rate': self.win_rate * 100,
                'volatility': self.returns.std() * np.sqrt(252) * 100
            }
            
        except Exception as e:
            logger.error(f"计算性能指标失败: {str(e)}")
            return {}
    
    def plot_performance(self) -> Optional[plt.Figure]:
        """绘制性能图表"""
        try:
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
            
            # 绘制累计收益曲线
            ax1.plot(self.cum_returns.index, self.cum_returns.values)
            ax1.set_title('累计收益曲线')
            ax1.grid(True)
            
            # 绘制回撤曲线
            rolling_max = self.cum_returns.expanding().max()
            drawdowns = (self.cum_returns / rolling_max - 1) * 100
            ax2.fill_between(drawdowns.index, drawdowns.values, 0, color='red', alpha=0.3)
            ax2.set_title('回撤曲线')
            ax2.grid(True)
            
            plt.tight_layout()
            return fig
            
        except Exception as e:
            logger.error(f"绘制性能图表失败: {str(e)}")
            return None
    
    def generate_report(self) -> str:
        """生成性能报告"""
        try:
            metrics = self.calculate_metrics()
            
            report = f"""
            策略性能报告
            ================
            年化收益率: {metrics['annual_return']:.2f}%
            最大回撤: {metrics['max_drawdown']:.2f}%
            夏普比率: {metrics['sharpe_ratio']:.2f}
            胜率: {metrics['win_rate']:.2f}%
            波动率: {metrics['volatility']:.2f}%
            
            交易统计
            ----------------
            总交易天数: {len(self.returns.dropna())}
            盈利天数: {(self.returns > 0).sum()}
            亏损天数: {(self.returns < 0).sum()}
            """
            
            return report
            
        except Exception as e:
            logger.error(f"生成性能报告失败: {str(e)}")
            return "性能报告生成失败" 