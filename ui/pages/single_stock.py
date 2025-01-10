import streamlit as st
from src.strategies.ma_strategy import MAStrategy
from src.data.data_loader import DataLoader

def render_single_stock_page():
    st.header("个股分析")
    
    # 移动原 app.py 中的单股分析相关代码
    symbol = st.text_input('股票代码', '600000')
    # ... 其他代码 