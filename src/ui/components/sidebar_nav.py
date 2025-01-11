import streamlit as st

def render_nav_tree(menu_items: list) -> str:
    """渲染导航树"""
    with st.sidebar:
        # 设置侧边栏样式
        st.markdown("""
            <style>
                section[data-testid="stSidebar"] {
                    background-color: #1a1c23;
                    min-width: 280px !important;
                    max-width: 280px !important;
                }
                section[data-testid="stSidebar"] > div {
                    padding: 0rem;
                    padding-bottom: 5rem;
                }
                
                /* Logo区域 */
                .logo-container {
                    padding: 2rem 1.5rem;
                    margin-bottom: 1rem;
                    border-bottom: 1px solid rgba(255,255,255,0.1);
                    background: linear-gradient(to right, rgba(49,130,206,0.1), transparent);
                }
                .logo-text {
                    color: #3182ce;
                    font-size: 1.25rem;
                    font-weight: 600;
                    letter-spacing: 0.025em;
                }
                
                /* 导航分组 */
                .nav-section {
                    margin-bottom: 1.5rem;
                    padding: 0 1rem;
                }
                .nav-header {
                    color: #718096;
                    font-size: 0.75rem;
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                    padding: 0.5rem;
                    margin-bottom: 0.5rem;
                    display: flex;
                    align-items: center;
                }
                .nav-header span {
                    margin-right: 0.5rem;
                }
                
                /* 导航按钮 */
                .stButton {
                    margin-bottom: 0.25rem;
                }
                .stButton button {
                    width: 100%;
                    background: transparent;
                    color: #e2e8f0;
                    border: none;
                    text-align: left;
                    font-size: 0.875rem;
                    padding: 0.625rem 1rem;
                    border-radius: 0.375rem;
                    transition: all 0.2s;
                    margin: 0;
                    display: flex;
                    align-items: center;
                }
                .stButton button:hover {
                    background: rgba(255,255,255,0.1);
                    color: white;
                }
                .stButton button::before {
                    content: "•";
                    margin-right: 0.75rem;
                    color: #718096;
                    font-size: 1.25rem;
                    line-height: 0;
                }
                
                /* 底部状态 */
                .status-bar {
                    position: fixed;
                    bottom: 0;
                    left: 0;
                    width: 280px;
                    padding: 1rem 1.5rem;
                    background-color: rgba(0,0,0,0.2);
                    border-top: 1px solid rgba(255,255,255,0.1);
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    z-index: 1000;
                }
                .status-dot {
                    width: 8px;
                    height: 8px;
                    border-radius: 50%;
                    background-color: #48bb78;
                    margin-right: 0.5rem;
                    display: inline-block;
                }
                .status-text {
                    color: #a0aec0;
                    font-size: 0.75rem;
                }
            </style>
        """, unsafe_allow_html=True)
        
        # Logo
        st.markdown("""
            <div class="logo-container">
                <span class="logo-text">量化策略平台</span>
            </div>
        """, unsafe_allow_html=True)
        
        # 导航菜单
        selected = None
        
        # 遍历菜单项
        for item in menu_items:
            st.markdown(f"""
                <div class="nav-section">
                    <div class="nav-header">
                        <span>{item['icon']}</span>
                        {item['name']}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # 遍历子菜单
            for child in item['children']:
                clicked = st.button(
                    child['name'],
                    key=child['id'],
                    help=child.get('description', ''),
                    use_container_width=True,
                )
                if clicked:
                    selected = child['id']
        
        # 底部状态栏
        st.markdown("""
            <div class="status-bar">
                <div style="display: flex; align-items: center;">
                    <span class="status-dot"></span>
                    <span class="status-text">系统运行正常</span>
                </div>
                <div style="display: flex; flex-direction: column; align-items: flex-end;">
                    <span class="status-text">v1.0.0</span>
                    <span class="status-text" style="font-size: 0.7rem; color: #718096;">
                        by 韦正海 (VX: devdiv)
                    </span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        return selected 