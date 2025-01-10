import streamlit as st
import matplotlib.pyplot as plt
from trading_strategy import MAStrategy

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

if __name__ == '__main__':
    main() 