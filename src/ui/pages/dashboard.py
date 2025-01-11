import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def render_dashboard():
    st.title("📊 市场概览")
    
    # 市场指数概览
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            "上证指数",
            "3,234.56",
            "0.86%",
            help="上证综合指数"
        )
    with col2:
        st.metric(
            "深证成指",
            "12,345.67",
            "-0.52%",
            help="深证成份指数"
        )
    with col3:
        st.metric(
            "创业板指",
            "2,345.67",
            "1.23%",
            help="创业板指数"
        )
    with col4:
        st.metric(
            "科创50",
            "1,234.56",
            "-0.78%",
            help="科创50指数"
        )
    
    # 市场热度分析
    st.subheader("市场热度分析")
    
    # 创建两列布局
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # 成交量分析
        dates = pd.date_range(start='2024-01-01', end='2024-01-10')
        volume_data = pd.DataFrame({
            'date': dates,
            'volume': np.random.uniform(5000, 8000, len(dates)),
            'ma5': np.random.uniform(6000, 7000, len(dates)),
            'ma10': np.random.uniform(6500, 7500, len(dates))
        })
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=volume_data['date'],
            y=volume_data['volume'],
            name='成交量',
            marker_color='rgba(49,130,206,0.7)'
        ))
        fig.add_trace(go.Scatter(
            x=volume_data['date'],
            y=volume_data['ma5'],
            name='5日均量',
            line=dict(color='#48bb78')
        ))
        fig.add_trace(go.Scatter(
            x=volume_data['date'],
            y=volume_data['ma10'],
            name='10日均量',
            line=dict(color='#ed8936')
        ))
        
        fig.update_layout(
            title='市场成交量趋势',
            height=400,
            margin=dict(t=30, b=0),
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # 市场情绪指标
        sentiment_data = pd.DataFrame({
            '指标': ['人气指标', '强弱指标', '恐慌指数', '活跃度'],
            '数值': [65, 58, 42, 78],
            '变化': [5, -3, -8, 12]
        })
        
        for _, row in sentiment_data.iterrows():
            st.metric(
                row['指标'],
                f"{row['数值']}",
                f"{row['变化']:+}",
                delta_color="normal"
            )
    
    # 行业板块热度
    st.subheader("行业板块热度")
    
    industries = ['科技', '医药', '金融', '消费', '制造', '能源', '材料']
    changes = np.random.uniform(-3, 3, len(industries))
    volumes = np.random.uniform(1000, 5000, len(industries))
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Bar(
            x=industries,
            y=changes,
            name="涨跌幅",
            marker_color=['red' if x > 0 else 'green' for x in changes]
        ),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(
            x=industries,
            y=volumes,
            name="成交额",
            line=dict(color='#4299e1')
        ),
        secondary_y=True
    )
    
    fig.update_layout(
        title='行业板块表现',
        height=400,
        margin=dict(t=30, b=0),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 市场资金流向
    st.subheader("市场资金流向")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # 资金流向图
        flow_data = pd.DataFrame({
            '时间': pd.date_range(start='2024-01-01', end='2024-01-10'),
            '主力净流入': np.random.uniform(-50, 50, 10),
            '散户净流入': np.random.uniform(-30, 30, 10),
            '北向资金': np.random.uniform(-40, 40, 10)
        })
        
        fig = go.Figure()
        
        for col in ['主力净流入', '散户净流入', '北向资金']:
            fig.add_trace(go.Scatter(
                x=flow_data['时间'],
                y=flow_data[col],
                name=col,
                fill='tonexty'
            ))
        
        fig.update_layout(
            height=300,
            margin=dict(t=0, b=0),
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # 资金流向统计
        st.dataframe(
            pd.DataFrame({
                '资金类型': ['主力资金', '散户资金', '北向资金'],
                '净流入': ['12.5亿', '-5.8亿', '8.3亿'],
                '变化': ['↑', '↓', '↑']
            }),
            hide_index=True
        ) 