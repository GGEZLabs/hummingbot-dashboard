import streamlit as st


def user_inputs():
    default_config = st.session_state.get("default_config", {})
    exchange = default_config.get("exchange", ["p2b", "coinstore", "uzx"])
    trading_pair = default_config.get("trading_pair", "ETH-USDT")
    refresh_time = default_config.get("refresh_time", 15)
    volume_threshold = default_config.get("volume_threshold", 1.0)

    with st.container():
        st.subheader("Volume Monitor Configuration")

        # For exchanges, we'll use a text area for now to allow flexibility,
        # or we could try to find a list of exchanges.
        # Given the requirement is a list of strings, let's use a multiselect
        # with the defaults provided and maybe some common ones, or just allow
        # the user to type them if we use a different widget.
        # But standard Streamlit multiselect needs a fixed list of options.
        # Let's use text_input and split by comma for simplicity and
        # flexibility unless we find a better component.
        # Actually, let's provide the requested defaults as options and allow
        # adding more?
        # Streamlit's multiselect allows adding new options if configured?
        # No, it doesn't by default.
        # Let's use a text_input with a help string.

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
        "exchange": exchange_list,
        "trading_pair": trading_pair,
        "refresh_time": refresh_time,
        "volume_threshold": volume_threshold,
        "script_file_name": "volume_monitor.py",
    }
