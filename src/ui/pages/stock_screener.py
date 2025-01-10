import streamlit as st
import pandas as pd
from src.ui.components import strategy_config

def render_screener_page(strategy_name: str):
    """渲染选股页面"""
    st.title(f"策略选股 - {strategy_name}")
    
    # 选股范围设置
    st.subheader("选股范围")
    col1, col2 = st.columns(2)
    with col1:
        market = st.multiselect(
            "市场",
            ["沪深300", "中证500", "创业板", "科创板"],
            ["沪深300"]
        )
        min_price = st.number_input("最低价格", value=5.0)
    with col2:
        industry = st.multiselect(
            "行业",
            ["全部"] + get_industry_list(),
            ["全部"]
        )
        max_price = st.number_input("最高价格", value=100.0)
    
    # 运行选股
    if st.button("开始选股", type="primary"):
        results = run_stock_screening(
            strategy_name,
            market,
            industry,
            min_price,
            max_price
        )
        display_screening_results(results)

def get_industry_list() -> list:
    """获取行业列表"""
    # TODO: 从数据源获取行业列表
    return [
        "银行", "证券", "保险", "房地产",
        "医药生物", "计算机", "电子", "通信",
        "机械设备", "电气设备", "化工", "有色金属"
    ]

def run_stock_screening(
    strategy_name: str,
    market: list,
    industry: list,
    min_price: float,
    max_price: float
) -> pd.DataFrame:
    """运行选股"""
    # TODO: 实现选股逻辑
    # 临时返回示例数据
    return pd.DataFrame({
        'stock_code': ['000001.SZ', '600000.SH', '300750.SZ'],
        'stock_name': ['平安银行', '浦发银行', '宁德时代'],
        'industry': ['银行', '银行', '电气设备'],
        'current_price': [20.5, 15.8, 380.2],
        'signal_strength': [0.85, 0.75, 0.92],
        'expected_return': [0.15, 0.12, 0.20],
        'risk_score': [0.35, 0.30, 0.45]
    })

def display_screening_results(results: pd.DataFrame):
    """显示选股结果"""
    if results.empty:
        st.warning("未找到符合条件的股票")
        return
        
    # 结果统计
    st.subheader(f"选股结果 - 共{len(results)}只股票")
    
    # 买入建议
    st.subheader("买入建议")
    st.dataframe(
        results,
        column_config={
            "stock_code": "股票代码",
            "stock_name": "股票名称",
            "industry": "所属行业",
            "current_price": "当前价格",
            "signal_strength": "信号强度",
            "expected_return": "预期收益",
            "risk_score": "风险评分"
        },
        use_container_width=True
    ) 