import unittest
import pandas as pd
import numpy as np
from src.strategies.trend_following import TrendFollowingStrategy
from src.indicators.momentum import MomentumIndicators
from src.utils.cache import Cache
from src.utils.risk_manager import RiskManager

class TestCore(unittest.TestCase):
    def setUp(self):
        # 创建测试数据
        dates = pd.date_range(start='2023-01-01', end='2023-12-31')
        self.test_data = pd.DataFrame({
            'open': np.random.randn(len(dates)).cumsum() + 100,
            'high': np.random.randn(len(dates)).cumsum() + 102,
            'low': np.random.randn(len(dates)).cumsum() + 98,
            'close': np.random.randn(len(dates)).cumsum() + 100,
            'volume': np.random.randint(1000, 10000, len(dates))
        }, index=dates)
    
    def test_trend_strategy(self):
        """测试趋势跟踪策略"""
        strategy = TrendFollowingStrategy()
        result = strategy.generate_signals(self.test_data)
        
        # 验证信号生成
        self.assertIn('signal', result.columns)
        self.assertIn('position_size', result.columns)
        
        # 验证信号值
        self.assertTrue(all(result['signal'].isin([-1, 0, 1])))
        
        # 验证持仓规模
        max_position = strategy.parameters['position_size']
        self.assertTrue(all(abs(result['position_size']) <= max_position))
    
    def test_momentum_indicators(self):
        """测试动量指标"""
        indicators = MomentumIndicators()
        
        # 测试RSI
        rsi = indicators.calculate_rsi(self.test_data['close'])
        self.assertTrue(all(rsi.between(0, 100)))
        
        # 测试MACD
        macd, signal, hist = indicators.calculate_macd(self.test_data['close'])
        self.assertEqual(len(macd), len(self.test_data))
    
    def test_risk_manager(self):
        """测试风险管理"""
        risk_manager = RiskManager()
        
        # 测试持仓限制
        self.assertTrue(risk_manager.check_position_limit(100000, 10000))
        self.assertFalse(risk_manager.check_position_limit(100000, 50000))
        
        # 测试止损
        self.assertTrue(risk_manager.check_stop_loss(100, 94))
        self.assertFalse(risk_manager.check_stop_loss(100, 96))

if __name__ == '__main__':
    unittest.main() 