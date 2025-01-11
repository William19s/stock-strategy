import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def render_technical_analysis():
    st.title("📊 技术分析")
    
    # 股票选择和时间范围
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        stock = st.selectbox(
            "选择股票",
            ["平安银行(000001)", "招商银行(600036)", "宁德时代(300750)"]
        )
    with col2:
        start_date = st.date_input("开始日期")
    with col3:
        end_date = st.date_input("结束日期")
    
    # 生成示例数据
    dates = pd.date_range(start=start_date, end=end_date)
    n_days = len(dates)
    
    # OHLCV数据
    price_data = pd.DataFrame({
        'date': dates,
        'open': np.random.normal(100, 2, n_days).cumsum(),
        'high': np.random.normal(101, 2, n_days).cumsum(),
        'low': np.random.normal(99, 2, n_days).cumsum(),
        'close': np.random.normal(100, 2, n_days).cumsum(),
        'volume': np.random.uniform(1000000, 5000000, n_days)
    })
    
    # 技术指标选择
    indicators = st.multiselect(
        "技术指标",
        ["MA", "MACD", "KDJ", "RSI", "BOLL"],
        ["MA", "MACD"]
    )
    
    # 创建子图
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.6, 0.2, 0.2]
    )
    
    # K线图
    fig.add_trace(
        go.Candlestick(
            x=price_data['date'],
            open=price_data['open'],
            high=price_data['high'],
            low=price_data['low'],
            close=price_data['close'],
            name="OHLC"
        ),
        row=1, col=1
    )
    
    # 成交量
    fig.add_trace(
        go.Bar(
            x=price_data['date'],
            y=price_data['volume'],
            name="成交量",
            marker_color='rgba(49,130,206,0.7)'
        ),
        row=2, col=1
    )
    
    # MACD
    macd = np.random.normal(0, 1, n_days).cumsum()
    signal = np.random.normal(0, 0.8, n_days).cumsum()
    hist = macd - signal
    
    fig.add_trace(
        go.Scatter(
            x=price_data['date'],
            y=macd,
            name="MACD",
            line=dict(color='#3182ce')
        ),
        row=3, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=price_data['date'],
            y=signal,
            name="Signal",
            line=dict(color='#ed8936')
        ),
        row=3, col=1
    )
    
    fig.add_trace(
        go.Bar(
            x=price_data['date'],
            y=hist,
            name="Histogram",
            marker_color=['red' if x > 0 else 'green' for x in hist]
        ),
        row=3, col=1
    )
    
    # 更新布局
    fig.update_layout(
        height=800,
        margin=dict(t=30, b=0),
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis_rangeslider_visible=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 技术分析结论
    st.subheader("分析结论")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 技术指标信号
        signals = pd.DataFrame({
            '指标': ['MA', 'MACD', 'KDJ', 'RSI', 'BOLL'],
            '信号': ['多头', '金叉', '超买', '中性', '突破'],
            '建议': ['买入', '买入', '卖出', '观望', '买入']
        })
        
        st.dataframe(signals, use_container_width=True)
    
    with col2:
        # 支撑压力位
        levels = pd.DataFrame({
            '类型': ['压力位1', '压力位2', '支撑位1', '支撑位2'],
            '价格': [105.2, 107.5, 98.5, 96.2],
            '强度': ['强', '中', '强', '中']
        })
        
        st.dataframe(levels, use_container_width=True) 