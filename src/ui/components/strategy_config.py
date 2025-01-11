import streamlit as st
from typing import Dict, Any

def render_strategy_params(strategy: Any) -> Dict:
    """渲染策略参数配置"""
    st.subheader("参数配置")
    
    params = {}
    
    # 根据策略类型显示不同的参数配置
    if strategy.name == "趋势跟踪策略":
        col1, col2 = st.columns(2)
        with col1:
            params['fast_ma'] = st.number_input(
                "快速均线周期",
                min_value=1,
                max_value=100,
                value=strategy.parameters['fast_ma']
            )
            params['slow_ma'] = st.number_input(
                "慢速均线周期",
                min_value=1,
                max_value=200,
                value=strategy.parameters['slow_ma']
            )
            params['atr_period'] = st.number_input(
                "ATR周期",
                min_value=1,
                max_value=100,
                value=strategy.parameters['atr_period']
            )
        
        with col2:
            params['atr_multiplier'] = st.number_input(
                "ATR倍数",
                min_value=0.1,
                max_value=5.0,
                value=strategy.parameters['atr_multiplier']
            )
            params['position_size'] = st.slider(
                "仓位比例",
                min_value=0.0,
                max_value=1.0,
                value=strategy.parameters['position_size']
            )
            params['stop_loss'] = st.slider(
                "止损比例",
                min_value=0.01,
                max_value=0.20,
                value=strategy.parameters['stop_loss']
            )
            params['take_profit'] = st.slider(
                "止盈比例",
                min_value=0.01,
                max_value=0.50,
                value=strategy.parameters['take_profit']
            )
    
    # 添加其他策略的参数配置...
    
    return params 