from datetime import datetime, timedelta

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from database.connector import fetch_market_data, fetch_price_change_summary, fetch_price_data
from frontend.st_utils import get_backend_api_client, initialize_st_page

initialize_st_page(layout="wide", show_readme=False)
backend_api_client = get_backend_api_client()

# Custom CSS for enhanced styling
st.markdown(
    """
    <style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }

    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        color: white;
    }

    .pulse {
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }

    .status-active {
        color: #4CAF50;
        font-weight: bold;
    }

    .status-inactive {
        color: #ff6b6b;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def get_all_bots_data():
    """Fetch all bots from the backend API"""
    try:
        bots_response = backend_api_client.bot_orchestration.get_active_bots_status()
        all_bots = {}
        if bots_response.get("status") == "success":
            bots = bots_response.get("data", {})
            for bot_name, bot_info in bots.items():
                try:
                    bot_status = backend_api_client.bot_orchestration.get_bot_status(bot_name)
                    if bot_status.get("status") == "success":
                        bot_data = bot_status.get("data", {})
                        bot_info["status"] = bot_data.get("status")
                        all_bots[bot_name] = bot_info
                except Exception:
                    continue
        return all_bots
    except Exception as e:
        st.error(f"Error fetching bots: {e}")
        return {}


def get_bot_status(bot_name):
    """Fetch the status of a specific bot"""
    try:
        bot_status_response = backend_api_client.bot_orchestration.get_bot_status(bot_name)
        if bot_status_response.get("status") == "success":
            return bot_status_response.get("data", {})
        else:
            st.error(f"Failed to fetch status for {bot_name}")
            return {}
    except Exception as e:
        st.error(f"Error fetching status for {bot_name}: {e}")
        return {}


# Quick Stats Dashboard
st.markdown("## 📊 Live Dashboard Overview")

# Fetch market data
market_data = fetch_market_data()

# Extract aggregated data
if market_data and market_data["market_aggregate"]["aggregate"]:
    aggregated_data = market_data["market_aggregate"]["aggregate"]
    total_volume = aggregated_data["sum"]["volume"]
    total_turnover = aggregated_data["sum"]["amount"]
    avg_price = aggregated_data["avg"]["price"]
    exchange_count = aggregated_data["count"]
else:
    total_volume = 0
    total_turnover = 0
    avg_price = 0
    exchange_count = 0


all_bots = get_all_bots_data()
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="metric-card">
            <h3>⚡ Total Volume</h3>
            <div class="stat-number">{total_volume:,.2f}</div>
            <p>GGEZ1</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class="metric-card">
            <h3>💰 Total Turn Over</h3>
            <div class="stat-number">${total_turnover:,.2f}</div>
            <p>USDT</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


with col3:
    st.markdown(
        f"""
        <div class="metric-card">
            <h3>📈 Current Price</h3>
            <div class="stat-number">{avg_price:,.4f}</div>
            <p>GGEZ1/USDT</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col4:
    st.markdown(
        f"""
        <div class="metric-card">
            <h3>🔄 Number of Exchanges</h3>
            <div class="stat-number pulse">{exchange_count}</div>
            <p>Currently Active</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()
# Price Change Summary
price_change_summary = fetch_price_change_summary(p_trading_pair="GGEZ1-USDT")
price_change_summary_data = {}
if price_change_summary and "market_price_change_summary" in price_change_summary:
    for summary in price_change_summary["market_price_change_summary"]:
        price_change_summary_data[summary["period"]] = summary["price_change_pct"]

st.markdown("### 📈 Price Change Summary")
col1, col2, col3, col4, col5, col6 = st.columns(6)
periods = ["1 Hour", "1 Day", "1 Week", "1 Month", "3 Month", "All Time"]

for col, period in zip([col1, col2, col3, col4, col5, col6], periods):
    with col:
        value = price_change_summary_data.get(period, 0)
        color = "green" if value >= 0 else "red"
        st.markdown(f"<h6>{period}</h6> <h3 style='color:{color}'>{value:.2f}%</h3>", unsafe_allow_html=True)

st.divider()
# Performance Chart
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📈 **GGEZ1-USDT** Price Performance (30 Days)")

    # Fetch and display real performance chart
    end_time = datetime.now()
    start_time = end_time - timedelta(days=30)

    price_data = fetch_price_data(
        p_time_interval="1 day",
        p_trading_pair="GGEZ1-USDT",
        p_start_time=start_time.isoformat(),
        p_end_time=end_time.isoformat(),
        p_exchange="average",
    )

    if price_data and "market_get_candlestick_data" in price_data and price_data["market_get_candlestick_data"]:
        candlestick_data = price_data["market_get_candlestick_data"]
        df = pd.DataFrame(candlestick_data)
        df["time_bucket"] = pd.to_datetime(df["time_bucket"])
        df["close_price"] = df["close_price"] * 10**-6

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=df["time_bucket"],
                y=df["close_price"],
                mode="lines+markers",
                line=dict(color="#4CAF50", width=3),
                # fill="tonexty",
                # fillcolor="rgba(76, 175, 80, 0.1)",
                name="Portfolio Value",
            )
        )

        fig.update_layout(
            template="plotly_dark",
            height=400,
            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)"),
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No performance data available for the last 30 days.")

with col2:
    st.markdown("### 🎯 Strategy Status")
    if not all_bots:
        st.markdown(
            """
            <div style="background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 8px; margin: 0.5rem 0;">
                <div style="display: flex; justify-content: center; align-items: center;">
                    <div>
                        <strong>No bots found.</strong><br>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        for bot_name, bot_info in all_bots.items():
            status = bot_info.get("status", "unknown")
            if status == "running":
                status_class = "status-active"
                status_icon = "🟢"
            else:
                status_class = "status-inactive"
                status_icon = "🔴"

            if "performance" in bot_info and bot_info["performance"]:
                for controller_name, controller_info in bot_info["performance"].items():
                    pnl = controller_info.get("performance", {}).get("global_pnl_pct", 0)
                    pnl_color = "#4CAF50" if pnl >= 0 else "#ff6b6b"

                    st.markdown(
                        f"""
                        <div style="background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 8px; margin: 0.5rem 0;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <strong>{controller_name.replace("_", " ").title()}</strong><br>
                                    <span class="{status_class}">{status_icon} {status.title()}</span>
                                </div>
                                <div style="text-align: right;">
                                    <span style="color: {pnl_color}; font-weight: bold;">{pnl:+.2f}%</span>
                                </div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            else:
                st.markdown(
                    f"""
                    <div style="background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 8px; margin: 0.5rem 0;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <strong>{bot_name.replace("_", " ").title()}</strong><br>
                                <span class="{status_class}">{status_icon} {status.title()}</span>
                            </div>
                            <div style="text-align: right;">
                                <span style="color: #4CAF50; font-weight: bold;">N/A</span>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

st.divider()
