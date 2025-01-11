import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def render_fundamental_analysis():
    st.title("📈 基本面分析")
    
    # 股票选择
    stock = st.selectbox(
        "选择股票",
        ["平安银行(000001)", "招商银行(600036)", "宁德时代(300750)"]
    )
    
    # 创建主布局
    tab1, tab2, tab3 = st.tabs(["财务分析", "估值分析", "行业对比"])
    
    with tab1:
        # 财务分析
        st.subheader("关键财务指标")
        
        # 财务指标概览
        metrics = st.columns(4)
        with metrics[0]:
            st.metric("营收增速", "15.8%", "2.3%")
        with metrics[1]:
            st.metric("净利率", "25.5%", "-1.2%")
        with metrics[2]:
            st.metric("ROE", "12.8%", "0.5%")
        with metrics[3]:
            st.metric("资产负债率", "65.2%", "-2.1%")
        
        # 财务报表趋势
        st.subheader("财务报表趋势")
        
        # 生成财务数据
        years = pd.date_range(start='2020', end='2024', freq='YE')
        financial_data = pd.DataFrame({
            '年份': years,
            '营业收入': np.random.normal(100, 10, len(years)).cumsum(),
            '净利润': np.random.normal(20, 5, len(years)).cumsum(),
            '经营现金流': np.random.normal(25, 5, len(years)).cumsum()
        })
        
        fig = go.Figure()
        
        for col in ['营业收入', '净利润', '经营现金流']:
            fig.add_trace(go.Scatter(
                x=financial_data['年份'],
                y=financial_data[col],
                name=col,
                mode='lines+markers'
            ))
        
        fig.update_layout(
            height=400,
            margin=dict(t=20, b=0),
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # 估值分析
        st.subheader("估值指标")
        
        # 估值指标
        valuation_metrics = st.columns(4)
        with valuation_metrics[0]:
            st.metric("市盈率(TTM)", "16.8", "-2.3")
        with valuation_metrics[1]:
            st.metric("市净率", "2.5", "0.2")
        with valuation_metrics[2]:
            st.metric("市销率", "3.2", "-0.1")
        with valuation_metrics[3]:
            st.metric("股息率", "2.8%", "0.3%")
        
        # 估值历史
        st.subheader("估值历史")
        
        dates = pd.date_range(start='2020-01-01', end='2024-01-01', freq='ME')
        valuation_history = pd.DataFrame({
            '日期': dates,
            'PE': np.random.normal(15, 2, len(dates)),
            'PB': np.random.normal(2, 0.3, len(dates)),
            'PS': np.random.normal(3, 0.5, len(dates))
        })
        
        fig = go.Figure()
        
        for col in ['PE', 'PB', 'PS']:
            fig.add_trace(go.Scatter(
                x=valuation_history['日期'],
                y=valuation_history[col],
                name=col
            ))
        
        fig.update_layout(
            height=400,
            margin=dict(t=20, b=0),
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        # 行业对比
        st.subheader("行业对比分析")
        
        # 行业排名
        industry_comparison = pd.DataFrame({
            '公司': ['平安银行', '招商银行', '建设银行', '工商银行', '交通银行'],
            '市值(亿)': [2500, 8500, 12000, 15000, 3500],
            'ROE': [12.5, 15.8, 13.2, 14.5, 11.8],
            '营收增速': [15.2, 18.5, 12.8, 11.5, 10.2],
            'PE': [16.8, 18.5, 15.2, 14.8, 13.5]
        })
        
        st.dataframe(
            industry_comparison,
            column_config={
                '市值(亿)': st.column_config.NumberColumn(
                    '市值(亿)',
                    format="%.0f"
                ),
                'ROE': st.column_config.NumberColumn(
                    'ROE',
                    format="%.1f%%"
                ),
                '营收增速': st.column_config.NumberColumn(
                    '营收增速',
                    format="%.1f%%"
                ),
                'PE': st.column_config.NumberColumn(
                    'PE',
                    format="%.1f"
                )
            },
            use_container_width=True
        )
        
        # 行业对比图
        st.subheader("主要指标行业对比")
        
        metrics = ['ROE', '营收增速', 'PE']
        companies = industry_comparison['公司'].tolist()
        
        fig = go.Figure()
        
        for metric in metrics:
            fig.add_trace(go.Bar(
                name=metric,
                x=companies,
                y=industry_comparison[metric],
                text=industry_comparison[metric].apply(lambda x: f'{x:.1f}'),
                textposition='auto',
            ))
        
        fig.update_layout(
            height=400,
            margin=dict(t=20, b=0),
            plot_bgcolor='white',
            paper_bgcolor='white',
            barmode='group'
        )
        
        st.plotly_chart(fig, use_container_width=True) 