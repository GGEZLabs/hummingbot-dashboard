import streamlit as st

from frontend.st_utils import get_backend_api_client, initialize_st_page

initialize_st_page(layout="wide", show_readme=False)
backend_api_client = get_backend_api_client()

# Custom CSS for enhanced styling
st.markdown(
    """
    <style>
    .feature-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1.5rem;
        backdrop-filter: blur(10px);
         margin: 1rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Hero Section
st.markdown(
    """
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="font-size: 3rem; margin-bottom: 0.5rem;">🤖 GGEZ1 Hummingbot Dashboard</h1>
        <p style="font-size: 1.2rem; color: #888; margin-bottom: 2rem;">
            Your Command Center for Algorithmic Trading Excellence
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# Feature Showcase
st.markdown("## 🚀 Platform Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
    <div class="feature-card">
        <div style="text-align: center; margin-bottom: 1rem;">
            <div style="font-size: 3rem;">🎯</div>
            <h3>Strategy Development</h3>
        </div>
        <ul style="list-style: none; padding: 0;">
            <li>✨ Visual Strategy Builder</li>
            <li>🔧 Advanced Configuration</li>
            <li>📝 Custom Parameters</li>
            <li>🧪 Testing Environment</li>
        </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
    <div class="feature-card">
        <div style="text-align: center; margin-bottom: 1rem;">
            <div style="font-size: 3rem;">📊</div>
            <h3>Analytics & Insights</h3>
        </div>
        <ul style="list-style: none; padding: 0;">
            <li>📈 Real-time Performance</li>
            <li>🔍 Advanced Backtesting</li>
            <li>📋 Detailed Reports</li>
            <li>🎨 Interactive Charts</li>
        </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
    <div class="feature-card">
        <div style="text-align: center; margin-bottom: 1rem;">
            <div style="font-size: 3rem;">⚡</div>
            <h3>Live Trading</h3>
        </div>
        <ul style="list-style: none; padding: 0;">
            <li>🤖 Automated Execution</li>
            <li>📡 Real-time Monitoring</li>
            <li>🛡️ Risk Management</li>
            <li>🔔 Smart Alerts</li>
        </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )


st.divider()

# Community & Resources
col1 = st.columns(1)[0]

with col1:
    st.markdown("### 💬 Join Our Community")
    st.markdown(
        """
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 1.5rem; border-radius: 15px; color: white; text-align: center;">
            <h4>🌟 GGEZ1 – Building the Future of Sustainable Web3</h4>
            <p>Join our ecosystem and explore tokenized sustainability assets!</p>
            <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; margin-top: 15px;">
                <a href="https://www.ggez.one/" target="_blank"
                style="flex: 1 1 30%; min-width: 120px; text-align: center;
                        background: rgba(255,255,255,0.2); padding: 0.6rem 1rem;
                        border-radius: 8px; text-decoration: none; color: white; font-weight: bold;">
                🌐 Website
                </a>
                <a href="https://x.com/ggez_one" target="_blank"
                style="flex: 1 1 30%; min-width: 120px; text-align: center;
                        background: rgba(255,255,255,0.2); padding: 0.6rem 1rem;
                        border-radius: 8px; text-decoration: none; color: white; font-weight: bold;">
                        <span style="color: black;">𝕏</span> Twitter
                </a>
                <a href="https://www.linkedin.com/company/ggezone" target="_blank"
                style="flex: 1 1 30%; min-width: 120px; text-align: center;
                        background: rgba(255,255,255,0.2); padding: 0.6rem 1rem;
                        border-radius: 8px; text-decoration: none; color: white; font-weight: bold;">
                💼 LinkedIn
                </a>
                <a href="https://www.facebook.com/ggez.one" target="_blank"
                style="flex: 1 1 30%; min-width: 120px; text-align: center;
                        background: rgba(255,255,255,0.2); padding: 0.6rem 1rem;
                        border-radius: 8px; text-decoration: none; color: white; font-weight: bold;">
                📘 Facebook
                </a>
                <a href="https://www.youtube.com/@ggez_one" target="_blank"
                style="flex: 1 1 30%; min-width: 120px; text-align: center;
                        background: rgba(255,255,255,0.2); padding: 0.6rem 1rem;
                        border-radius: 8px; text-decoration: none; color: white; font-weight: bold;">
                ▶️ YouTube
                </a>
                <a href="https://t.me/ggez1live" target="_blank"
                style="flex: 1 1 30%; min-width: 120px; text-align: center;
                        background: rgba(255,255,255,0.2); padding: 0.6rem 1rem;
                        border-radius: 8px; text-decoration: none; color: white; font-weight: bold;">
                📢 Telegram
                </a>
                <a href="https://www.instagram.com/ggez.one/" target="_blank"
                style="flex: 1 1 30%; min-width: 120px; text-align: center;
                        background: rgba(255,255,255,0.2); padding: 0.6rem 1rem;
                        border-radius: 8px; text-decoration: none; color: white; font-weight: bold;">
                📸 Instagram
                </a>
                <a href="https://discord.com/invite/7P4RvsEeMA" target="_blank"
                style="flex: 1 1 30%; min-width: 120px; text-align: center;
                        background: rgba(255,255,255,0.2); padding: 0.6rem 1rem;
                        border-radius: 8px; text-decoration: none; color: white; font-weight: bold;">
                💬 Discord
                </a>
                <a href="https://github.com/GGEZLabs" target="_blank"
                style="flex: 1 1 30%; min-width: 120px; text-align: center;
                        background: rgba(255,255,255,0.2); padding: 0.6rem 1rem;
                        border-radius: 8px; text-decoration: none; color: white; font-weight: bold;">
                🧑‍💻 GitHub
                </a>
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )
