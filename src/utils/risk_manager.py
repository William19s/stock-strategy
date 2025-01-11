import pandas as pd
from typing import Dict, Optional
from .logger import setup_logger

logger = setup_logger(__name__)

class RiskManager:
    """风险管理器"""
    
    def __init__(self):
        self.max_position_ratio = 0.2  # 单个持仓最大比例
        self.max_drawdown = 0.1        # 最大回撤限制
        self.stop_loss_ratio = 0.05    # 止损比例
        self.take_profit_ratio = 0.15  # 止盈比例
    
    def check_position_limit(self, capital: float, position_value: float) -> bool:
        """检查持仓限制"""
        try:
            position_ratio = position_value / capital
            return position_ratio <= self.max_position_ratio
        except Exception as e:
            logger.error(f"持仓检查失败: {str(e)}")
            return False
    
    def get_max_position_size(self, capital: float) -> float:
        """获取最大持仓规模"""
        return capital * self.max_position_ratio
    
    def check_stop_loss(self, entry_price: float, current_price: float) -> bool:
        """检查止损"""
        try:
            if entry_price <= 0:
                return False
            return (entry_price - current_price) / entry_price >= self.stop_loss_ratio
        except Exception as e:
            logger.error(f"止损检查失败: {str(e)}")
            return False
    
    def check_take_profit(self, entry_price: float, current_price: float) -> bool:
        """检查止盈"""
        try:
            if entry_price <= 0:
                return False
            return (current_price - entry_price) / entry_price >= self.take_profit_ratio
        except Exception as e:
            logger.error(f"止盈检查失败: {str(e)}")
            return False
    
    def check_drawdown(self, equity_curve: pd.Series) -> bool:
        """检查回撤"""
        try:
            if equity_curve.empty:
                return False
            rolling_max = equity_curve.expanding().max()
            drawdown = (rolling_max - equity_curve) / rolling_max
            return drawdown.max() <= self.max_drawdown
        except Exception as e:
            logger.error(f"回撤检查失败: {str(e)}")
            return False 