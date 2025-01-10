import streamlit as st
import matplotlib.pyplot as plt
from trading_strategy import MAStrategy
import pandas as pd

def show_overview():
    st.markdown("""
    ## 📈 策略概述
    这是一个基于移动平均线的股票交易策略分析工具。
    
    ### 主要功能
    - 双均线交易策略回测
    - 策略收益可视化
    - 交易信号分析
    
    ### 使用说明
    1. 输入股票代码（例如：AAPL）
    2. 调整短期和长期MA周期
    3. 点击"运行策略"查看结果
    """)

def plot_strategy(df, short_window, long_window):
    # 创建图表
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # 绘制股价和移动平均线
    ax1.plot(df.index, df['Close'], label='股价', alpha=0.7)
    ax1.plot(df.index, df['SMA_short'], label=f'{short_window}日MA', alpha=0.7)
    ax1.plot(df.index, df['SMA_long'], label=f'{long_window}日MA', alpha=0.7)
    ax1.set_title('股价与移动平均线')
    ax1.legend()
    
    # 绘制累计收益对比
    ax2.plot(df.index, df['Cumulative_Returns'], label='买入持有', alpha=0.7)
    ax2.plot(df.index, df['Strategy_Cumulative_Returns'], label='策略收益', alpha=0.7)
    ax2.set_title('策略收益对比')
    ax2.legend()
    
    return fig

def add_strategy_analysis(results):
    st.write("### 策略分析")
    
    # 计算关键指标
    total_trades = len(results[results['Signal'].diff() != 0])
    win_rate = (results['Strategy_Returns'] > 0).mean() * 100
    max_drawdown = ((results['Strategy_Cumulative_Returns'].cummax() - results['Strategy_Cumulative_Returns']) 
                    / results['Strategy_Cumulative_Returns'].cummax()).max() * 100
    
    # 显示指标
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("总交易次数", f"{total_trades}次")
    with col2:
        st.metric("胜率", f"{win_rate:.2f}%")
    with col3:
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
        symbol = st.text_input('输入股票代码（例如：AAPL）', 'AAPL')
        short_window = st.slider('短期MA周期', 5, 50, 20)
        long_window = st.slider('长期MA周期', 20, 200, 50)

        if st.button('运行策略'):
            # 运行策略
            strategy = MAStrategy(symbol, short_window, long_window)
            results = strategy.backtest()
            
            if results is not None:
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

if __name__ == '__main__':
    main() 