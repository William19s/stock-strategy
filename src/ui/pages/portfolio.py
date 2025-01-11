import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def render_portfolio():
    st.title("📈 投资组合管理")
    
    # 创建主布局
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # 组合概览
        st.subheader("组合概览")
        
        # 组合基本信息
        metrics_cols = st.columns(4)
        with metrics_cols[0]:
            st.metric("总资产", "￥1,234,567", "2.3%")
        with metrics_cols[1]:
            st.metric("持仓市值", "￥986,543", "1.8%")
        with metrics_cols[2]:
            st.metric("可用资金", "￥248,024", "-5.2%")
        with metrics_cols[3]:
            st.metric("持仓收益", "￥34,567", "12.5%")
        
        # 持仓明细
        st.subheader("持仓明细")
        holdings = pd.DataFrame({
            '股票代码': ['000001', '600036', '300750', '601318'],
            '股票名称': ['平安银行', '招商银行', '宁德时代', '中国平安'],
            '持仓数量': [10000, 8000, 2000, 5000],
            '成本价': [18.5, 45.6, 280.5, 65.8],
            '现价': [19.2, 44.8, 295.6, 68.2],
            '市值': [192000, 358400, 591200, 341000],
            '盈亏': [7000, -6400, 30200, 12000],
            '仓位': ['15.5%', '29.0%', '47.8%', '27.6%']
        })
        
        st.dataframe(
            holdings,
            column_config={
                '股票代码': st.column_config.TextColumn('股票代码'),
                '持仓数量': st.column_config.NumberColumn('持仓数量', format="%d"),
                '成本价': st.column_config.NumberColumn('成本价', format="%.2f"),
                '现价': st.column_config.NumberColumn('现价', format="%.2f"),
                '市值': st.column_config.NumberColumn('市值', format="%.0f"),
                '盈亏': st.column_config.NumberColumn(
                    '盈亏',
                    format="%.0f",
                    help="持仓盈亏金额"
                )
            },
            use_container_width=True
        )
        
        # 收益走势
        st.subheader("收益走势")
        dates = pd.date_range(start='2024-01-01', end='2024-01-31')
        returns = np.random.normal(0.001, 0.02, len(dates)).cumsum()
        benchmark = np.random.normal(0.0005, 0.015, len(dates)).cumsum()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates,
            y=returns,
            name="组合收益",
            line=dict(color='#3182ce')
        ))
        fig.add_trace(go.Scatter(
            x=dates,
            y=benchmark,
            name="基准收益",
            line=dict(color='#718096', dash='dash')
        ))
        
        fig.update_layout(
            height=400,
            margin=dict(t=20, b=0),
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # 组合操作
        st.subheader("组合操作")
        
        # 交易操作
        with st.form("trade_form"):
            stock_code = st.text_input("股票代码")
            trade_type = st.selectbox("交易类型", ["买入", "卖出"])
            price = st.number_input("价格", min_value=0.0, format="%.3f")
            quantity = st.number_input("数量", min_value=0, step=100)
            
            submitted = st.form_submit_button("提交交易")
            if submitted:
                st.success("交易提交成功！")
        
        # 仓位分布
        st.subheader("仓位分布")
        
        # 行业分布
        industry_dist = pd.DataFrame({
            '行业': ['金融', '科技', '消费', '医药'],
            '占比': [35, 25, 20, 20]
        })
        
        fig = go.Figure(data=[go.Pie(
            labels=industry_dist['行业'],
            values=industry_dist['占比'],
            hole=.3
        )])
        
        fig.update_layout(
            height=300,
            margin=dict(t=0, b=0),
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 风险提示
        st.info("""
        风险提示：
        - 当前组合波动率：15.2%
        - 最大回撤：-8.5%
        - 夏普比率：1.85
        """) 