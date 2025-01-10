import streamlit as st
from datetime import datetime
import psutil

def render_nav_tree(menu_items: list) -> str:
    """渲染导航树"""
    with st.sidebar:
        # 顶部标题和LOGO
        col1, col2 = st.columns([1, 4])
        with col1:
            # 暂时注释掉logo
            # st.image("assets/logo.png", width=50)
            st.write("📈")
        with col2:
            st.title("策略分析系统")
        
        # 搜索框
        st.text_input("🔍 搜索策略", key="strategy_search")
        
        # 渲染菜单项
        selected = None
        for item in menu_items:
            st.subheader(f"{item['icon']} {item['name']}")
            for child in item['children']:
                if st.button(
                    child['name'],
                    key=child['id'],
                    use_container_width=True
                ):
                    selected = child['id']
        
        # 底部信息
        st.markdown("---")
        st.caption("© 2024 策略分析系统")
        
        return selected 