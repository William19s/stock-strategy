import streamlit as st

def render_strategy_overview():
    """渲染策略概述页面"""
    st.header("策略说明")
    
    st.markdown("""
    ## 交易策略说明
    
    ### 1. 均线交叉策略
    - 短期均线上穿长期均线形成金叉买入
    - MACD指标确认趋势
    - RSI指标过滤超买超卖
    - KDJ指标辅助确认
    
    ### 2. 交易条件
    - 市值范围：80亿-500亿
    - 股价条件：>5元
    - 成交量条件：大于5日均量
    
    ### 3. 风险控制
    - RSI超买区间卖出
    - 均线死叉卖出
    - 设置止损位
    """) 