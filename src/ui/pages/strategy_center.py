import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def render_config_page(strategy_name: str):
    """渲染策略配置页面"""
    
    # 页面标题和描述
    st.title(f"📊 {strategy_name}")
    
    # 创建两列布局
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # 策略回测区域
        with st.container():
            st.subheader("策略回测")
            
            # 回测参数设置
            params_container = st.container()
            with params_container:
                col1, col2, col3 = st.columns(3)
                with col1:
                    start_date = st.date_input("开始日期")
                with col2:
                    end_date = st.date_input("结束日期")
                with col3:
                    initial_capital = st.number_input("初始资金(万)", value=100)
            
            # 股票池设置
            stock_pool = st.multiselect(
                "选择股票池",
                ["沪深300", "中证500", "创业板", "科创板"],
                ["沪深300"]
            )
            
            # 回测按钮
            if st.button("开始回测", type="primary", use_container_width=True):
                with st.spinner("回测中..."):
                    # 生成回测数据
                    dates = pd.date_range(start=start_date, end=end_date)
                    returns = np.random.normal(0.001, 0.02, len(dates)).cumsum()
                    benchmark = np.random.normal(0.0005, 0.015, len(dates)).cumsum()
                    
                    # 回测结果图表
                    fig = make_subplots(
                        rows=2, cols=1,
                        subplot_titles=("策略收益", "持仓分析"),
                        vertical_spacing=0.12,
                        row_heights=[0.7, 0.3]
                    )
                    
                    # 收益曲线
                    fig.add_trace(
                        go.Scatter(
                            x=dates,
                            y=returns,
                            name="策略收益",
                            line=dict(color="#3182ce")
                        ),
                        row=1, col=1
                    )
                    fig.add_trace(
                        go.Scatter(
                            x=dates,
                            y=benchmark,
                            name="基准收益",
                            line=dict(color="#718096", dash="dash")
                        ),
                        row=1, col=1
                    )
                    
                    # 持仓分析
                    holdings = ["平安银行", "贵州茅台", "宁德时代", "腾讯控股", "招商银行"]
                    weights = np.random.uniform(0.1, 0.3, len(holdings))
                    weights = weights / weights.sum()
                    
                    fig.add_trace(
                        go.Bar(
                            x=holdings,
                            y=weights,
                            name="持仓权重",
                            marker_color="#3182ce"
                        ),
                        row=2, col=1
                    )
                    
                    fig.update_layout(
                        height=600,
                        showlegend=True,
                        plot_bgcolor="white",
                        paper_bgcolor="white"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # 回测指标
                    metrics_cols = st.columns(4)
                    with metrics_cols[0]:
                        st.metric("年化收益", "15.8%", "5.2%")
                    with metrics_cols[1]:
                        st.metric("最大回撤", "-12.5%", "2.1%")
                    with metrics_cols[2]:
                        st.metric("夏普比率", "1.85", "0.3")
                    with metrics_cols[3]:
                        st.metric("胜率", "62.5%", "4.5%")
    
    with col2:
        # 策略参数设置
        with st.container():
            st.subheader("参数设置")
            
            # 参数分组
            tabs = st.tabs(["基础参数", "高级参数", "风控参数"])
            
            with tabs[0]:
                st.number_input("MA快线周期", value=5)
                st.number_input("MA慢线周期", value=20)
                st.number_input("ATR周期", value=14)
            
            with tabs[1]:
                st.slider("开仓阈值", 0.0, 1.0, 0.7)
                st.slider("平仓阈值", 0.0, 1.0, 0.3)
                st.number_input("信号确认周期", value=3)
            
            with tabs[2]:
                st.slider("止损比例", 0.0, 0.2, 0.05)
                st.slider("止盈比例", 0.0, 0.5, 0.15)
                st.number_input("最大持仓数", value=10)
        
        # 参数模板
        with st.container():
            st.subheader("参数模板")
            col1, col2 = st.columns([3, 1])
            with col1:
                st.text_input(
                    label="模板名称",
                    value="新模板",
                    key="template_name",
                    label_visibility="visible"
                )
            with col2:
                st.button("保存模板", use_container_width=True)
        
        # 策略说明
        with st.container():
            st.subheader("策略说明")
            st.markdown("""
                - 策略类型：趋势跟踪
                - 适用市场：A股市场
                - 交易标的：股票
                - 建议资金：100万以上
                - 更新时间：每日收盘后
            """)
            
            with st.expander("查看更多说明"):
                st.markdown("""
                    #### 策略逻辑
                    1. 使用双均线系统判断趋势方向
                    2. 结合ATR进行波动率分析
                    3. 设置动态止损止盈位置
                    
                    #### 注意事项
                    - 建议在趋势明确的市场环境下使用
                    - 需要注意调整参数以适应不同的市场情况
                    - 建议结合其他指标进行交叉验证
                """) 