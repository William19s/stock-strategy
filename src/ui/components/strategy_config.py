import streamlit as st
import pandas as pd
from src.strategies.base_strategy import BaseStrategy

def render_strategy_params(strategy: BaseStrategy):
    """渲染策略参数配置"""
    
    # 参数分组显示
    tabs = st.tabs(["基础参数", "高级参数", "风控参数"])
    
    with tabs[0]:
        col1, col2 = st.columns(2)
        basic_params = {k: v for k, v in strategy.parameters.items() 
                       if not k.startswith(('advanced_', 'risk_'))}
        _render_params_group(basic_params, col1, col2)
    
    with tabs[1]:
        col1, col2 = st.columns(2)
        advanced_params = {k: v for k, v in strategy.parameters.items() 
                         if k.startswith('advanced_')}
        _render_params_group(advanced_params, col1, col2)
    
    with tabs[2]:
        col1, col2 = st.columns(2)
        risk_params = {k: v for k, v in strategy.parameters.items() 
                      if k.startswith('risk_')}
        _render_params_group(risk_params, col1, col2)
    
    # 参数模板
    st.markdown("#### 参数模板")
    col1, col2, col3 = st.columns([2,2,1])
    with col1:
        template = st.selectbox(
            "选择模板",
            ["默认参数", "保守策略", "激进策略", "自定义方案1", "自定义方案2"]
        )
    with col2:
        st.text_input("模板名称", value="新模板")
    with col3:
        st.button("保存模板", use_container_width=True)
    
    # 参数验证
    if not strategy.validate_parameters():
        st.error("⚠️ 参数验证失败，请检查参数设置")
        return False
    
    return True

def _render_params_group(params: dict, col1, col2):
    """渲染参数组"""
    col_idx = 0
    for param_name, param_value in params.items():
        with col1 if col_idx % 2 == 0 else col2:
            # 美化参数名显示
            display_name = param_name.replace('_', ' ').title()
            
            if isinstance(param_value, bool):
                params[param_name] = st.checkbox(
                    display_name,
                    value=param_value,
                    key=f"param_{param_name}"
                )
            elif isinstance(param_value, int):
                params[param_name] = st.number_input(
                    display_name,
                    min_value=1,
                    value=param_value,
                    key=f"param_{param_name}",
                    help=f"参数说明: {param_name}"  # 添加参数说明
                )
            elif isinstance(param_value, float):
                params[param_name] = st.number_input(
                    display_name,
                    min_value=0.0,
                    value=param_value,
                    format="%.3f",
                    key=f"param_{param_name}",
                    help=f"参数说明: {param_name}"  # 添加参数说明
                )
            elif isinstance(param_value, (list, tuple)):
                params[param_name] = st.multiselect(
                    display_name,
                    options=param_value,
                    default=param_value,
                    key=f"param_{param_name}"
                )
        col_idx += 1 