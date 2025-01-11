import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.data.market_data import MarketData

def render_screening_page():
    """渲染策略选股页面"""
    st.title("策略选股")
    
    # 选股参数设置
    with st.expander("选股参数", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("技术指标")
            # 1. 均线策略
            ma_enabled = st.checkbox("均线策略", True)
            if ma_enabled:
                ma_short = st.slider("短期均线", 5, 30, 20)
                ma_long = st.slider("长期均线", 30, 120, 60)
            
            # 2. MACD策略
            macd_enabled = st.checkbox("MACD策略")
            if macd_enabled:
                macd_fast = st.slider("MACD快线", 5, 20, 12)
                macd_slow = st.slider("MACD慢线", 20, 40, 26)
            
            # 3. RSI策略
            rsi_enabled = st.checkbox("RSI策略")
            if rsi_enabled:
                rsi_period = st.slider("RSI周期", 6, 24, 14)
                rsi_upper = st.slider("RSI上限", 50, 90, 70)
                rsi_lower = st.slider("RSI下限", 10, 50, 30)
            
            # 4. KDJ策略
            kdj_enabled = st.checkbox("KDJ策略")
            if kdj_enabled:
                k_period = st.slider("K周期", 5, 20, 9)
                d_period = st.slider("D周期", 2, 10, 3)
            
            # 5. 布林带策略
            boll_enabled = st.checkbox("布林带策略")
            if boll_enabled:
                boll_period = st.slider("布林带周期", 10, 30, 20)
                boll_std = st.slider("标准差倍数", 1.0, 3.0, 2.0)
        
        with col2:
            st.subheader("基本面指标")
            # 6. 市值指标
            market_cap = st.slider("市值范围（亿）", 0, 10000, (100, 5000))
            
            # 7. 估值指标
            pe_range = st.slider("市盈率范围", 0, 100, (0, 50))
            pb_range = st.slider("市净率范围", 0, 20, (0, 10))
            
            # 8. 成长指标
            revenue_growth = st.slider("营收增长率(%)", -50, 100, (0, 50))
            profit_growth = st.slider("净利润增长率(%)", -50, 100, (0, 50))
            
            # 9. 质量指标
            roe = st.slider("ROE范围(%)", 0, 50, (8, 30))
            debt_ratio = st.slider("资产负债率(%)", 0, 100, (0, 70))
            
            # 10. 行业选择
            industry = st.multiselect(
                "行业选择",
                ["金融", "科技", "医药", "消费", "地产", "新能源", "半导体", 
                 "机械", "农业", "建筑", "交通", "传媒", "军工", "环保"],
                ["科技", "医药", "新能源"]
            )
    
    # 执行选股
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("开始选股", type="primary"):
            try:
                market_data = MarketData()
                
                # 收集筛选条件
                criteria = {
                    'ma_enabled': ma_enabled,
                    'ma_short': ma_short if ma_enabled else None,
                    'ma_long': ma_long if ma_enabled else None,
                    'macd_enabled': macd_enabled,
                    'macd_fast': macd_fast if macd_enabled else None,
                    'macd_slow': macd_slow if macd_enabled else None,
                    'rsi_enabled': rsi_enabled,
                    'rsi_period': rsi_period if rsi_enabled else None,
                    'rsi_upper': rsi_upper if rsi_enabled else None,
                    'rsi_lower': rsi_lower if rsi_enabled else None,
                    'market_cap': market_cap,
                    'pe_range': pe_range,
                    'pb_range': pb_range,
                    'roe': roe,
                    'debt_ratio': debt_ratio,
                    'industry': industry
                }
                
                # 执行选股
                results = market_data.screen_stocks(criteria)
                
                if not results.empty:
                    st.success(f"选股完成！找到 {len(results)} 只符合条件的股票")
                    st.dataframe(results)
                else:
                    st.warning("没有找到符合条件的股票")
                    
            except Exception as e:
                st.error(f"选股失败: {str(e)}") 