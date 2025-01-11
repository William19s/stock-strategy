import pandas as pd
import numpy as np
from typing import Optional
from .base_strategy import BaseStrategy
from ..indicators.technical import TechnicalIndicators
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class MomentumStrategy(BaseStrategy):
    """动量策略"""
    
    def __init__(self, symbol: str, lookback: int = 20, holding_period: int = 5):
        super().__init__(symbol)
        self.params = {
            'lookback': lookback,  # 回看期
            'holding_period': holding_period,  # 持有期
            'momentum_threshold': 0  # 动量阈值
        }
        self.tech = TechnicalIndicators()
        
    def validate_parameters(self) -> bool:
        """验证策略参数"""
        try:
            if not isinstance(self.params['lookback'], int) or self.params['lookback'] <= 0:
                logger.error("回看期必须是正整数")
                return False
            if not isinstance(self.params['holding_period'], int) or self.params['holding_period'] <= 0:
                logger.error("持有期必须是正整数")
                return False
            return True
        except Exception as e:
            logger.error(f"参数验证失败: {str(e)}")
            return False
    
    def calculate_momentum(self, data: pd.DataFrame) -> pd.Series:
        """计算动量指标"""
        try:
            # 计算过去N日收益率
            returns = data['close'].pct_change(self.params['lookback'])
            
            # 计算动量得分
            momentum = returns.rolling(window=self.params['lookback']).mean()
            
            # 标准化动量得分
            momentum = (momentum - momentum.mean()) / momentum.std()
            
            return momentum
        except Exception as e:
            logger.error(f"动量计算失败: {str(e)}")
            return pd.Series()
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """生成交易信号"""
        try:
            # 计算动量
            momentum = self.calculate_momentum(data)
            
            # 生成信号
            signals = pd.Series(0, index=data.index)
            signals[momentum > self.params['momentum_threshold']] = 1  # 做多信号
            signals[momentum < -self.params['momentum_threshold']] = -1  # 做空信号
            
            # 应用持有期
            if self.params['holding_period'] > 1:
                signals = self._apply_holding_period(signals)
            
            data['signal'] = signals
            return data
            
        except Exception as e:
            logger.error(f"信号生成失败: {str(e)}")
            return pd.DataFrame()
    
    def _apply_holding_period(self, signals: pd.Series) -> pd.Series:
        """应用持有期"""
        try:
            held_positions = pd.Series(0, index=signals.index)
            current_position = 0
            holding_days = 0
            
            for i in range(len(signals)):
                if holding_days >= self.params['holding_period']:
                    # 持有期结束，可以更新仓位
                    if signals.iloc[i] != 0:
                        current_position = signals.iloc[i]
                        holding_days = 0
                    else:
                        current_position = 0
                else:
                    # 在持有期内
                    holding_days += 1
                
                held_positions.iloc[i] = current_position
            
            return held_positions
            
        except Exception as e:
            logger.error(f"持有期应用失败: {str(e)}")
            return signals
    
    def optimize_parameters(self, data: pd.DataFrame) -> dict:
        """优化策略参数"""
        try:
            best_sharpe = -np.inf
            best_params = self.params.copy()
            
            # 参数网格搜索
            for lookback in range(10, 60, 10):
                for holding in range(1, 10, 2):
                    self.params['lookback'] = lookback
                    self.params['holding_period'] = holding
                    
                    # 运行回测
                    result = self.run_strategy(data=data)
                    if result is None:
                        continue
                    
                    # 计算夏普比率
                    returns = result['close'].pct_change()
                    sharpe = np.sqrt(252) * returns.mean() / returns.std()
                    
                    if sharpe > best_sharpe:
                        best_sharpe = sharpe
                        best_params = self.params.copy()
            
            return best_params
            
        except Exception as e:
            logger.error(f"参数优化失败: {str(e)}")
            return self.params 