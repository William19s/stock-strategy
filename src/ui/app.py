import streamlit as st
from src.ui.components.sidebar_nav import render_nav_tree
from src.ui.components.strategy_config import render_config_page
from src.ui.pages.stock_screener import render_screener_page
from src.ui.pages.portfolio import render_portfolio
from src.ui.pages.portfolio_analysis import render_portfolio_analysis
from src.ui.pages.dashboard import render_dashboard
from src.ui.pages.technical_analysis import render_technical_analysis
from src.ui.pages.fundamental_analysis import render_fundamental_analysis
from src.ui.pages.risk_management import render_risk_management
from src.ui.pages.strategy_center import render_strategy_center

def main():
    """主应用入口"""
    st.set_page_config(
        page_title="策略分析系统",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 设置页面样式
    st.markdown("""
        <style>
            .block-container {
                padding-top: 1rem;
                padding-bottom: 0rem;
            }
        </style>
    """, unsafe_allow_html=True)

    # 定义菜单项
    menu_items = [
        {
            'icon': '📊',
            'name': '数据中心',
            'children': [
                {
                    'id': 'dashboard',
                    'name': '仪表盘',
                    'description': '市场概览'
                },
                {
                    'id': 'technical_analysis',
                    'name': '技术分析',
                    'description': '技术指标分析'
                },
                {
                    'id': 'fundamental_analysis',
                    'name': '基本面分析',
                    'description': '基本面数据分析'
                }
            ]
        },
        {
            'icon': '💡',
            'name': '策略中心',
            'children': [
                {
                    'id': 'strategy_center',
                    'name': '策略管理',
                    'description': '管理交易策略'
                },
                {
                    'id': 'stock_screener',
                    'name': '股票筛选',
                    'description': '多维度选股'
                }
            ]
        },
        {
            'icon': '📈',
            'name': '投资组合',
            'children': [
                {
                    'id': 'portfolio',
                    'name': '组合管理',
                    'description': '管理投资组合'
                },
                {
                    'id': 'portfolio_analysis',
                    'name': '组合分析',
                    'description': '分析组合表现'
                },
                {
                    'id': 'risk_management',
                    'name': '风险管理',
                    'description': '风险控制'
                }
            ]
        }
    ]
    
    # 页面路由
    selected = render_nav_tree(menu_items)
    
    # 根据选择渲染对应页面
    if not selected:
        render_dashboard()
    else:
        if selected == 'dashboard':
            render_dashboard()
        elif selected == 'technical_analysis':
            render_technical_analysis()
        elif selected == 'fundamental_analysis':
            render_fundamental_analysis()
        elif selected == 'strategy_center':
            render_strategy_center()
        elif selected == 'stock_screener':
            render_screener_page('股票筛选')
        elif selected == 'portfolio':
            render_portfolio()
        elif selected == 'portfolio_analysis':
            render_portfolio_analysis()
        elif selected == 'risk_management':
            render_risk_management()

if __name__ == "__main__":
    main() 