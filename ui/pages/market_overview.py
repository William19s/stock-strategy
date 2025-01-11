import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.data.market_data import MarketData

def render_market_overview():
    """渲染市场概览页面"""
    st.title("市场概览")
    
    # 初始化数据
    market_data = MarketData()
    
    # 1. 市场指标概览
    st.subheader("主要指数")
    col1, col2, col3 = st.columns(3)
    
    try:
        indices = market_data.get_market_overview()
        with col1:
            st.metric(
                label="上证指数",
                value=f"{indices['上证指数']['value']:,.2f}",
                delta=f"{indices['上证指数']['change']:.2f}%"
            )
        with col2:
            st.metric(
                label="深证成指",
                value=f"{indices['深证成指']['value']:,.2f}",
                delta=f"{indices['深证成指']['change']:.2f}%"
            )
        with col3:
            st.metric(
                label="创业板指",
                value=f"{indices['创业板指']['value']:,.2f}",
                delta=f"{indices['创业板指']['change']:.2f}%"
            )
    except Exception as e:
        st.error(f"获取市场数据失败: {str(e)}")
    
    # 2. 市场热度分析
    st.subheader("市场热度")
    tab1, tab2 = st.tabs(["行业板块", "概念板块"])
    
    with tab1:
        try:
            industry_data = market_data.get_industry_data()
            if not industry_data.empty:
                # 使用 matplotlib 绘制热力图
                plt.figure(figsize=(10, 6))
                plt.bar(industry_data.index, industry_data['change_pct'])
                plt.xticks(rotation=45)
                plt.title("行业板块涨跌分布")
                plt.tight_layout()
                st.pyplot(plt)
                plt.close()
                
                # 显示详细数据
                st.dataframe(industry_data)
        except Exception as e:
            st.error(f"获取行业数据失败: {str(e)}")
    
    # 3. 市场统计
    st.subheader("市场统计")
    col1, col2 = st.columns(2)
    
    with col1:
        try:
            breadth = market_data.get_market_breadth()
            # 使用 matplotlib 绘制柱状图
            plt.figure(figsize=(8, 5))
            colors = ['red', 'green', 'gray']
            plt.bar(['上涨', '下跌', '平盘'], 
                   [breadth['up'], breadth['down'], breadth['flat']],
                   color=colors)
            plt.title("涨跌家数")
            plt.tight_layout()
            st.pyplot(plt)
            plt.close()
        except Exception as e:
            st.error(f"获取市场统计失败: {str(e)}") 