import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def render_risk_management():
    st.title("🛡️ 风险管理")
    
    # 风险概览
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            "组合Beta",
            "0.85",
            "-0.05",
            help="相对于市场的系统性风险"
        )
    with col2:
        st.metric(
            "波动率",
            "15.2%",
            "-1.2%",
            help="年化波动率"
        )
    with col3:
        st.metric(
            "最大回撤",
            "-12.5%",
            "2.1%",
            help="历史最大回撤"
        )
    with col4:
        st.metric(
            "在险价值",
            "2.5%",
            "-0.3%",
            help="95%置信区间下的日VaR"
        )
    
    # 创建主布局
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # 风险分解
        st.subheader("风险分解")
        
        # 风险来源分析
        risk_sources = pd.DataFrame({
            '风险来源': ['市场风险', '行业风险', '个股风险', '风格风险', '其他风险'],
            '贡献度': [40, 25, 20, 10, 5],
            '变化': [2, -1, 1, -0.5, -0.2]
        })
        
        fig = go.Figure(data=[
            go.Bar(
                x=risk_sources['风险来源'],
                y=risk_sources['贡献度'],
                marker_color='#3182ce',
                text=risk_sources['贡献度'].apply(lambda x: f'{x}%'),
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            height=300,
            margin=dict(t=20, b=0),
            plot_bgcolor='white',
            paper_bgcolor='white',
            yaxis_title='风险贡献度(%)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 风险趋势
        st.subheader("风险趋势")
        
        # 生成风险指标趋势数据
        dates = pd.date_range(start='2024-01-01', end='2024-01-31')
        risk_data = pd.DataFrame({
            'date': dates,
            'volatility': np.random.normal(15, 2, len(dates)),
            'var': np.random.normal(2.5, 0.3, len(dates)),
            'beta': np.random.normal(0.85, 0.05, len(dates))
        })
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Scatter(
                x=risk_data['date'],
                y=risk_data['volatility'],
                name="波动率",
                line=dict(color='#3182ce')
            ),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(
                x=risk_data['date'],
                y=risk_data['var'],
                name="VaR",
                line=dict(color='#e53e3e')
            ),
            secondary_y=True
        )
        
        fig.update_layout(
            height=300,
            margin=dict(t=20, b=0),
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # 风险控制
        st.subheader("风险控制")
        
        with st.form("risk_control"):
            # 仓位控制
            st.markdown("##### 仓位控制")
            max_position = st.slider(
                "单一持仓上限",
                0, 100, 20,
                format="%d%%",
                help="单只股票的最大持仓比例"
            )
            
            max_industry = st.slider(
                "行业持仓上限",
                0, 100, 35,
                format="%d%%",
                help="单一行业的最大持仓比例"
            )
            
            # 止盈止损
            st.markdown("##### 止盈止损")
            stop_loss = st.slider(
                "止损线",
                -50, 0, -15,
                format="%d%%",
                help="触发止损的亏损比例"
            )
            
            take_profit = st.slider(
                "止盈线",
                0, 100, 30,
                format="%d%%",
                help="触发止盈的收益比例"
            )
            
            # 波动控制
            st.markdown("##### 波动控制")
            max_volatility = st.slider(
                "波动率上限",
                0, 50, 20,
                format="%d%%",
                help="可接受的最大年化波动率"
            )
            
            # 保存设置
            if st.form_submit_button("保存设置"):
                st.success("风控参数设置已更新！")
        
        # 风险预警
        st.subheader("风险预警")
        
        alerts = pd.DataFrame({
            '类型': ['止损预警', '仓位预警', '波动预警', '行业预警'],
            '标的': ['平安银行', '招商银行', '组合整体', '金融行业'],
            '详情': [
                '接近止损线(-12.5%)',
                '超过单一持仓限制',
                '波动率超过预设值',
                '行业配置过重'
            ]
        })
        
        st.dataframe(
            alerts,
            column_config={
                '类型': st.column_config.TextColumn(
                    '预警类型',
                    help="风险预警类型"
                ),
                '标的': st.column_config.TextColumn(
                    '预警标的',
                    help="触发预警的标的"
                ),
                '详情': st.column_config.TextColumn(
                    '预警详情',
                    help="预警具体信息"
                )
            },
            use_container_width=True
        ) 