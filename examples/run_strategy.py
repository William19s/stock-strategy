import pandas as pd
from datetime import datetime, timedelta
from src.data.market_data import MarketData
from src.strategies.trend_following import TrendFollowingStrategy
from src.utils.logger import setup_logger
from src.utils.profiler import profile

logger = setup_logger(__name__)

@profile
def run_strategy_example():
    """运行策略示例"""
    try:
        # 1. 初始化数据和策略
        market_data = MarketData()
        strategy = TrendFollowingStrategy()
        
        # 2. 获取测试数据
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
        
        data = market_data.get_history_data(
            code="sh.000001",  # 上证指数
            start_date=start_date,
            end_date=end_date
        )
        
        if data.empty:
            logger.error("获取数据失败")
            return
            
        # 3. 生成交易信号
        result = strategy.generate_signals(data)
        
        # 4. 计算策略绩效
        metrics = strategy.get_performance_metrics(result)
        
        # 5. 输出结果
        logger.info("策略参数:")
        for key, value in strategy.parameters.items():
            logger.info(f"- {key}: {value}")
            
        logger.info("\n策略绩效:")
        for key, value in metrics.items():
            logger.info(f"- {key}: {value:.2f}")
        
        # 6. 保存结果
        result.to_csv("strategy_results.csv")
        logger.info("\n结果已保存到 strategy_results.csv")
        
    except Exception as e:
        logger.error(f"策略运行失败: {str(e)}")

if __name__ == "__main__":
    run_strategy_example() 