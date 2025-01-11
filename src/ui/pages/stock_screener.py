import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def render_screener_page(title: str):
    st.title(f"🔍 {title}")
    
    # 创建主布局
    main_col1, main_col2 = st.columns([2, 1])
    
    with main_col1:
        # 筛选条件设置
        st.subheader("筛选条件")
        
        # 市场和行业选择
        markets = st.multiselect(
            "市场范围",
            ["沪深300", "中证500", "创业板", "科创板"],
            ["沪深300"]
        )
        
        industries = st.multiselect(
            "行业选择",
            ["金融", "科技", "医药", "消费", "制造", "能源", "材料"],
            ["科技", "医药"]
        )
        
        # 使用container替代嵌套columns
        with st.container():
            # 价格和市盈率
            price_range = st.slider(
                "股价范围",
                0.0, 100.0, (10.0, 50.0)
            )
            pe_range = st.slider(
                "市盈率范围",
                0.0, 100.0, (5.0, 30.0)
            )
            
            # 市值和ROE
            market_cap = st.multiselect(
                "市值范围",
                ["小盘股", "中盘股", "大盘股"]
            )
            roe_range = st.slider(
                "ROE范围(%)",
                0.0, 50.0, (8.0, 25.0)
            )
            
            # 成交量和换手率
            volume_range = st.slider(
                "成交量(万手)",
                0, 1000, (100, 500)
            )
            turnover_range = st.slider(
                "换手率(%)",
                0.0, 20.0, (2.0, 10.0)
            )
        
        # 技术指标
        tech_indicators = st.multiselect(
            "技术指标",
            ["MA5上穿MA10", "MACD金叉", "KDJ超买", "RSI超卖", "布林带突破"],
            ["MA5上穿MA10"]
        )
        
        # 开始筛选按钮
        if st.button("开始筛选", type="primary", use_container_width=True):
            # 生成示例数据
            stocks = pd.DataFrame({
                "股票代码": [f"{i:06d}" for i in range(1, 11)],
                "股票名称": [f"示例股票{i}" for i in range(1, 11)],
                "现价": np.random.uniform(10, 50, 10),
                "涨跌幅": np.random.uniform(-5, 5, 10),
                "换手率": np.random.uniform(2, 10, 10),
                "市盈率": np.random.uniform(5, 30, 10),
                "市值": np.random.uniform(100, 1000, 10),
                "ROE": np.random.uniform(8, 25, 10),
                "所属行业": np.random.choice(["科技", "医药", "金融"], 10)
            })
            
            # 显示结果
            st.dataframe(
                stocks,
                column_config={
                    "股票代码": st.column_config.TextColumn(
                        "股票代码",
                        help="点击查看详情"
                    ),
                    "现价": st.column_config.NumberColumn(
                        "现价",
                        format="%.2f"
                    ),
                    "涨跌幅": st.column_config.NumberColumn(
                        "涨跌幅",
                        format="%.2f%%"
                    ),
                    "换手率": st.column_config.NumberColumn(
                        "换手率",
                        format="%.2f%%"
                    ),
                    "市盈率": st.column_config.NumberColumn(
                        "市盈率",
                        format="%.2f"
                    ),
                    "市值": st.column_config.NumberColumn(
                        "市值",
                        format="%.2f亿"
                    ),
                    "ROE": st.column_config.NumberColumn(
                        "ROE",
                        format="%.2f%%"
                    )
                },
                use_container_width=True
            )
    
    with main_col2:
        # 选股方案
        st.subheader("选股方案")
        
        # 方案选择
        strategy = st.selectbox(
            "选择方案",
            ["自定义方案", "成长股策略", "价值股策略", "技术突破策略"]
        )
        
        # 保存方案
        with st.container():
            name = st.text_input(
                label="方案名称",
                value="新方案",
                key="strategy_name",
                label_visibility="visible"
            )
            st.button("保存方案", use_container_width=True)
        
        # 筛选统计
        st.subheader("筛选统计")
        
        # 生成行业分布数据
        industry_dist = pd.DataFrame({
            "行业": ["科技", "医药", "金融", "消费", "制造"],
            "数量": np.random.randint(5, 20, 5)
        })
        
        # 绘制行业分布图
        fig = go.Figure(data=[
            go.Bar(
                x=industry_dist["行业"],
                y=industry_dist["数量"],
                marker_color="#3182ce"
            )
        ])
        
        fig.update_layout(
            height=300,
            margin=dict(t=20, b=20, l=20, r=20),
            plot_bgcolor="white",
            paper_bgcolor="white"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 显示统计指标
        with st.container():
            st.metric("筛选结果数", "125只")
            st.metric("平均市盈率", "16.8")
            st.metric("平均市值", "158.5亿")
            st.metric("平均ROE", "12.5%") 