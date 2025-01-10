import streamlit as st
from src.ui.components.sidebar_nav import render_nav_tree
from src.ui.pages.strategy_center import render_config_page
from src.ui.pages.stock_screener import render_screener_page

def main():
    """主应用入口"""
    st.set_page_config(
        page_title="股票交易策略分析系统",
        page_icon="📈",
        layout="wide"
    )

    # 侧边栏导航
    menu_items = [
        {
            'name': '策略中心',
            'icon': '🎯',
            'children': [
                {'id': 'trend_following', 'name': '趋势跟踪策略'},
                {'id': 'volume_breakout', 'name': '量价突破策略'},
                {'id': 'ml_strategy', 'name': '机器学习策略'},
                {'id': 'factor_strategy', 'name': '多因子策略'}
            ]
        },
        {
            'name': '选股分析',
            'icon': '🔍',
            'children': [
                {'id': 'stock_screener', 'name': '策略选股'},
                {'id': 'stock_analysis', 'name': '个股分析'}
            ]
        }
    ]
    
    selected = render_nav_tree(menu_items)
    
    # 页面路由
    if selected:
        if selected == 'trend_following':
            render_config_page('趋势跟踪策略')
        elif selected == 'volume_breakout':
            render_config_page('量价突破策略')
        elif selected == 'ml_strategy':
            render_config_page('机器学习策略')
        elif selected == 'factor_strategy':
            render_config_page('多因子策略')
        elif selected == 'stock_screener':
            render_screener_page('策略选股')
        elif selected == 'stock_analysis':
            st.info('个股分析功能开发中...')

if __name__ == "__main__":
    main() 