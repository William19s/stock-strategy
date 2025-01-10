import streamlit as st
import matplotlib.pyplot as plt
from trading_strategy import MAStrategy
import pandas as pd

def show_overview():
    st.markdown("""
    ## 📈 策略概述
    这是一个基于移动平均线的股票交易策略分析工具。
    
    ### 股票代码说明
    - 上证主板：600xxx
    - 科创板：688xxx
    - 深证主板：000xxx、001xxx、003xxx
    - 中小板：002xxx
    - 创业板：300xxx
    """)

def plot_strategy(df, short_window, long_window):
    # 调整图表大小和布局以适应移动设备
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))  # 改为垂直布局
    plt.tight_layout(pad=3.0)  # 增加图表间距
    
    # 绘制股价和移动平均线
    ax1.plot(df.index, df['Close'], label='股价', alpha=0.7)
    ax1.plot(df.index, df['SMA_short'], label=f'{short_window}日MA', alpha=0.7)
    ax1.plot(df.index, df['SMA_long'], label=f'{long_window}日MA', alpha=0.7)
    ax1.set_title('股价与移动平均线')
    ax1.legend(loc='upper left', bbox_to_anchor=(0, -0.1))  # 调整图例位置
    ax1.tick_params(axis='x', rotation=45)  # 旋转x轴标签
    
    # 绘制累计收益对比
    ax2.plot(df.index, df['Cumulative_Returns'], label='买入持有', alpha=0.7)
    ax2.plot(df.index, df['Strategy_Cumulative_Returns'], label='策略收益', alpha=0.7)
    ax2.set_title('策略收益对比')
    ax2.legend(loc='upper left')
    ax2.tick_params(axis='x', rotation=45)
    
    return fig

def add_strategy_analysis(results):
    st.write("### 策略分析")
    
    # 使用容器来确保移动端显示正常
    with st.container():
        # 计算关键指标
        total_trades = len(results[results['Signal'].diff() != 0])
        win_rate = (results['Strategy_Returns'] > 0).mean() * 100
        max_drawdown = ((results['Strategy_Cumulative_Returns'].cummax() - results['Strategy_Cumulative_Returns']) 
                        / results['Strategy_Cumulative_Returns'].cummax()).max() * 100
        
        # 在移动端使用垂直布局
        st.metric("总交易次数", f"{total_trades}次")
        st.metric("胜率", f"{win_rate:.2f}%")
        st.metric("最大回撤", f"{max_drawdown:.2f}%")

def add_optimization():
    st.sidebar.write("### 参数优化")
    optimize = st.sidebar.checkbox("启用参数优化")
    
    if optimize:
        short_range = range(5, 50, 5)
        long_range = range(20, 200, 20)
        results = []
        
        progress_bar = st.sidebar.progress(0)
        for short in short_range:
            for long in long_range:
                if short < long:
                    strategy = MAStrategy(symbol, short, long)
                    result = strategy.backtest()
                    if result is not None:
                        final_return = (result['Strategy_Cumulative_Returns'].iloc[-1] - 1) * 100
                        results.append({'short': short, 'long': long, 'return': final_return})
        
        # 显示优化结果
        if results:
            results_df = pd.DataFrame(results)
            best_params = results_df.loc[results_df['return'].idxmax()]
            st.sidebar.write(f"最优参数：")
            st.sidebar.write(f"短期MA: {best_params['short']}")
            st.sidebar.write(f"长期MA: {best_params['long']}")

def main():
    # 设置页面配置以适应移动设备
    st.set_page_config(
        page_title="股票策略分析器",
        layout="wide",
        initial_sidebar_state="collapsed"  # 在移动端默认收起侧边栏
    )
    
    # 添加CSS样式
    st.markdown("""
        <style>
        .stApp {
            max-width: 100%;
            padding: 1rem;
        }
        .stPlot {
            width: 100%;
            height: auto;
        }
        .streamlit-expanderHeader {
            font-size: 1em;
        }
        @media (max-width: 640px) {
            .stMetric {
                width: 100%;
                margin-bottom: 1rem;
            }
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title('股票交易策略分析器')
    
    # 侧边栏用于导航
    page = st.sidebar.radio(
        "选择页面",
        ["策略概述", "策略回测"]
    )
    
    if page == "策略概述":
        show_overview()
    
    elif page == "策略回测":
        # 用户输入
        symbol = st.text_input('输入股票代码（例如：600000）', '600000')
        short_window = st.slider('短期MA周期', 5, 50, 20)
        long_window = st.slider('长期MA周期', 20, 200, 50)

        if st.button('运行策略'):
            # 运行策略
            strategy = MAStrategy(symbol, short_window, long_window)
            stock_name = strategy.get_stock_name()
            
            if stock_name:
                st.write(f"### 股票：{stock_name}（{symbol}）")
            
            results = strategy.backtest()
            
            if results is not None and not results.empty:  # 添加检查
                # 显示策略收益
                final_return = (results['Strategy_Cumulative_Returns'].iloc[-1] - 1) * 100
                st.write(f'策略最终收益：{final_return:.2f}%')
                
                # 显示图表
                fig = plot_strategy(results, short_window, long_window)
                st.pyplot(fig)
                
                # 显示详细数据
                st.write('### 交易数据')
                st.dataframe(results.tail())

                add_strategy_analysis(results)
            else:
                st.error(f"无法获取股票 {symbol} 的数据，请检查股票代码是否正确。")

if __name__ == '__main__':
    main() 