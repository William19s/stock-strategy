import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.data.market_data import MarketData
from src.utils.validators import validate_stock_code

def render_single_stock_page():
    """渲染个股分析页面"""
    st.title("个股分析")
    
    # 股票选择和基本信息
    col1, col2 = st.columns([2, 3])
    
    with col1:
        # 股票选择
        symbol = st.text_input("股票代码", "sh.600000")
        if not validate_stock_code(symbol):
            st.error("请输入正确的股票代码")
            return
        
        if st.button("获取数据"):
            try:
                market_data = MarketData()
                stock_info = market_data.get_stock_info(symbol)
                if stock_info:
                    st.success("数据获取成功！")
                    
                    # 显示基本信息
                    st.subheader("基本信息")
                    metrics = {
                        "最新价": f"¥{stock_info['close']:.2f}",
                        "涨跌幅": f"{stock_info['change_pct']:.2f}%",
                        "换手率": f"{stock_info['turnover_rate']:.2f}%",
                        "市盈率": f"{stock_info['pe_ratio']:.2f}",
                        "市值": f"{stock_info['market_cap']:.0f}亿"
                    }
                    for key, value in metrics.items():
                        st.metric(key, value)
            except Exception as e:
                st.error(f"获取数据失败: {str(e)}")
    
    with col2:
        # K线图和技术指标
        if 'stock_data' in st.session_state:
            plot_stock_chart(st.session_state.stock_data)
    
    # 策略分析
    if 'stock_data' in st.session_state:
        st.subheader("策略分析")
        
        # 策略参数设置
        with st.expander("策略参数", expanded=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                ma_short = st.slider("短期均线", 5, 30, 20)
            with col2:
                ma_long = st.slider("长期均线", 30, 120, 60)
            with col3:
                st.selectbox("其他指标", ["MACD", "RSI", "KDJ"])

def plot_stock_chart(data: pd.DataFrame):
    """绘制股票K线图"""
    plt.figure(figsize=(12, 6))
    
    # 绘制K线图
    plt.plot(data.index, data['close'], label='收盘价')
    plt.title("股票走势图")
    plt.xlabel("日期")
    plt.ylabel("价格")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    st.pyplot(plt)
    plt.close() 