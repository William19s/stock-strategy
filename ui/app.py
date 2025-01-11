import streamlit as st
from ui.pages.market_overview import render_market_overview
from ui.pages.single_stock import render_single_stock_page
from ui.pages.screening import render_screening_page
import pandas as pd
import atexit

def cleanup():
    """清理资源"""
    if 'market_data' in st.session_state:
        try:
            del st.session_state.market_data
        except:
            pass

def main():
    """主应用入口"""
    # 注册清理函数
    atexit.register(cleanup)
    
    try:
        st.set_page_config(
            page_title="股票策略分析器",
            page_icon="📈",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # 侧边栏 - 系统导航
        with st.sidebar:
            st.title("股票策略分析器")
            
            # 用户设置区
            with st.expander("⚙️ 系统设置", expanded=False):
                st.selectbox("选择数据源", ["BaoStock", "TuShare", "离线数据"])
                st.date_input("默认起始日期", value=pd.to_datetime('2020-01-01'))
            
            # 主导航
            page = st.radio(
                "功能导航",
                options=["市场概览", "个股分析", "策略选股"],
                format_func=lambda x: {
                    "市场概览": "📊 市场概览",
                    "个股分析": "🔍 个股分析",
                    "策略选股": "📈 策略选股"
                }[x]
            )
            
            # 底部信息
            st.sidebar.markdown("---")
            st.sidebar.markdown("### 关于")
            st.sidebar.info(
                "本工具用于股票策略分析和回测。"
                "数据来源: BaoStock"
            )
        
        # 主页面路由
        if page == "市场概览":
            render_market_overview()
        elif page == "个股分析":
            render_single_stock_page()
        else:
            render_screening_page()
    except Exception as e:
        st.error(f"应用运行错误: {str(e)}")
    finally:
        cleanup()

if __name__ == '__main__':
    main() 