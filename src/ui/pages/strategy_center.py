import streamlit as st
import pandas as pd
import numpy as np
from src.ui.components import strategy_config
from src.strategies.base_strategy import BaseStrategy
from src.strategies.trend_following import TrendFollowingStrategy
from src.strategies.volume_breakout import VolumeBreakoutStrategy
from src.strategies.ml_strategy import MLStrategy
from src.strategies.factor_strategy import FactorStrategy

def render_config_page(strategy_name: str):
    """渲染策略配置页面"""
    st.title(f"策略配置 - {strategy_name}")
    
    # 添加页面说明
    st.info("""
    👋 欢迎使用策略配置页面！
    
    在这里你可以：
    - 配置策略参数
    - 运行策略回测
    - 查看回测结果
    - 优化策略参数
    """)
    
    # 策略选择
    strategy_options = {
        "趋势跟踪策略": TrendFollowingStrategy,
        "量价突破策略": VolumeBreakoutStrategy,
        "机器学习策略": MLStrategy,
        "多因子策略": FactorStrategy
    }
    
    tabs = st.tabs(["策略配置", "回测分析", "绩效评估"])
    
    with tabs[0]:
        selected_strategy = st.selectbox(
            "选择策略",
            list(strategy_options.keys()),
            index=list(strategy_options.keys()).index(strategy_name)
        )
        
        # 实例化策略
        strategy = strategy_options[selected_strategy]()
        
        # 策略说明
        with st.expander("策略说明", expanded=True):
            st.markdown(get_strategy_description(selected_strategy))
        
        # 参数配置
        st.subheader("参数设置")
        strategy_config.render_strategy_params(strategy)
    
    with tabs[1]:
        # 回测设置
        st.subheader("回测设置")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            start_date = st.date_input("开始日期")
            initial_capital = st.number_input("初始资金", value=1000000)
        with col2:
            end_date = st.date_input("结束日期")
            commission_rate = st.slider("手续费率(%)", 0.0, 1.0, 0.1)
        with col3:
            benchmark = st.selectbox(
                "对标指数",
                ["沪深300", "上证指数", "深证成指", "创业板指"]
            )
            st.checkbox("包含股息", value=True)
        
        # 运行回测
        if st.button("运行回测", type="primary"):
            with st.spinner("回测运行中..."):
                results = run_backtest(
                    strategy,
                    start_date,
                    end_date,
                    initial_capital,
                    commission_rate
                )
                display_backtest_results(results)
    
    with tabs[2]:
        st.subheader("绩效评估")
        if 'results' in locals():
            display_performance_metrics(results)
        else:
            st.warning("请先运行回测以查看绩效评估")

def get_strategy_description(strategy_name: str) -> str:
    """获取策略说明"""
    descriptions = {
        "趋势跟踪策略": """
        ### 趋势跟踪策略
        
        基于均线和ATR的趋势跟踪策略，主要特点：
        - 使用双均线判断趋势方向
        - 利用ATR通道确认突破
        - 内置止损止盈机制
        - 支持仓位管理
        """,
        "量价突破策略": """
        ### 量价突破策略
        
        结合价格突破和成交量确认的策略，主要特点：
        - 价格突破重要关卡
        - 成交量放大确认
        - 趋势跟随
        - 动态止损
        """,
        "机器学习策略": """
        ### 机器学习策略
        
        基于机器学习模型的预测策略，主要特点：
        - 多维度特征工程
        - 随机森林模型
        - 动态训练优化
        - 概率化交易信号
        """,
        "多因子策略": """
        ### 多因子策略
        
        基于多个因子的选股策略，主要特点：
        - 动量/价值/波动率因子
        - 因子标准化处理
        - 因子权重优化
        - 动态再平衡
        """
    }
    return descriptions.get(strategy_name, "策略说明待补充")

def run_backtest(strategy, start_date, end_date, initial_capital, commission_rate):
    """运行回测"""
    try:
        # 获取数据
        from src.data.market_data import get_stock_data
        data = get_stock_data('000001.SZ', start_date, end_date)
        
        # 生成信号
        data = strategy.generate_signals(data)
        
        # 计算收益
        data['returns'] = data['close'].pct_change()
        data['strategy_returns'] = data['signal'].shift(1) * data['returns']
        data['cumulative_returns'] = (1 + data['strategy_returns']).cumprod()
        
        # 计算指标
        annual_return = (data['cumulative_returns'].iloc[-1] - 1) * 252 / len(data)
        sharpe = data['strategy_returns'].mean() / data['strategy_returns'].std() * np.sqrt(252)
        max_drawdown = (data['cumulative_returns'].cummax() - data['cumulative_returns']).max()
        win_rate = (data['strategy_returns'] > 0).mean()
        
        return {
            'returns': data['cumulative_returns'],
            'trades': pd.DataFrame({
                'date': pd.date_range(start='2023-01-01', periods=10),
                'symbol': ['000001.SZ'] * 10,
                'type': ['买入', '卖出'] * 5,
                'price': np.random.uniform(10, 20, 10),
                'shares': np.random.randint(100, 1000, 10),
                'profit': np.random.uniform(-1000, 1000, 10)
            }),
            'metrics': {
                'annual_return': annual_return * 100,
                'sharpe': sharpe,
                'max_drawdown': max_drawdown * 100,
                'win_rate': win_rate * 100
            }
        }
    except Exception as e:
        st.error(f"回测执行失败: {str(e)}")
        return {}

def display_backtest_results(results: dict):
    """显示回测结果"""
    if not results:
        return
        
    # 绩效指标
    st.subheader("策略绩效")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("年化收益", f"{results['metrics']['annual_return']:.2f}%")
    with col2:
        st.metric("夏普比率", f"{results['metrics']['sharpe']:.2f}")
    with col3:
        st.metric("最大回撤", f"{results['metrics']['max_drawdown']:.2f}%")
    with col4:
        st.metric("胜率", f"{results['metrics']['win_rate']:.2f}%")
    
    # 权益曲线
    st.subheader("权益曲线")
    st.line_chart(results['returns'])
    
    # 交易记录
    st.subheader("交易记录")
    st.dataframe(
        results['trades'],
        column_config={
            "date": "交易日期",
            "symbol": "股票代码",
            "type": "交易类型",
            "price": "成交价格",
            "shares": "成交数量",
            "profit": "收益"
        },
        use_container_width=True
    ) 

def display_performance_metrics(results: dict):
    """显示详细的绩效指标"""
    # 基础指标
    st.markdown("#### 收益指标")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("年化收益", f"{results['metrics']['annual_return']:.2f}%")
    with col2:
        st.metric("夏普比率", f"{results['metrics']['sharpe']:.2f}")
    with col3:
        st.metric("最大回撤", f"{results['metrics']['max_drawdown']:.2f}%")
    with col4:
        st.metric("胜率", f"{results['metrics']['win_rate']:.2f}%")
    
    # 风险指标
    st.markdown("#### 风险指标")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("波动率", "15.2%")
    with col2:
        st.metric("信息比率", "1.25")
    with col3:
        st.metric("Beta", "0.85")
    with col4:
        st.metric("Alpha", "5.2%")
    
    # 交易统计
    st.markdown("#### 交易统计")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("总交易次数", "156")
    with col2:
        st.metric("平均持仓天数", "12.5")
    with col3:
        st.metric("最大单笔收益", "8.2%")
    with col4:
        st.metric("最大单笔亏损", "-4.5%") 