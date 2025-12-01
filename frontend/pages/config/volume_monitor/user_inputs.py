import streamlit as st

from frontend.components.script_config_loader import get_script_config


def user_inputs(script_name: str = None):
    if script_name:
        default_config = get_script_config(script_name)
    else:
        default_config = st.session_state.get("default_config", {})
        exchange = default_config.get("exchange", ["p2b", "coinstore", "uzx"])
        trading_pair = default_config.get("trading_pair", "GGEZ1-USDT")
        refresh_time = default_config.get("refresh_time", 300)
        volume_threshold = default_config.get("volume_threshold", 50000.0)

        with st.container():
            st.subheader("Volume Monitor Configuration")

            exchange_str = st.text_input(
                "Exchanges (comma separated)",
                value=",".join(exchange) if isinstance(exchange, list) else exchange,
                help="List of exchanges to monitor, e.g., p2b, coinstore, uzx",
            )
            exchange_list = [e.strip() for e in exchange_str.split(",") if e.strip()]

            trading_pair = st.text_input("Trading Pair", value=trading_pair)

            c1, c2 = st.columns(2)
            with c1:
                refresh_time = st.number_input("Refresh Time (seconds)", min_value=1, value=int(refresh_time))
            with c2:
                volume_threshold = st.number_input("Volume Threshold", min_value=0.0, value=float(volume_threshold), step=0.1)

    return {
        "exchanges": exchange_list,
        "trading_pair": trading_pair,
        "refresh_time": refresh_time,
        "volume_threshold": volume_threshold,
        "script_file_name": "volume_monitor.py",
    }
