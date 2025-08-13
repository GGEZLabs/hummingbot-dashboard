import streamlit as st

from frontend.components.volume_pumper_general_inputs import get_volume_pumper_general_inputs


def user_inputs():
    default_config = st.session_state.get("default_config", {})
    (
        exchange,
        trading_pair,
        order_lower_amount,
        order_upper_amount,
        delay_order_time,
        max_random_delay,
        balance_loss_threshold,
        minimum_ask_bid_spread,
        periodic_report_interval,
    ) = get_volume_pumper_general_inputs()

    config = {
        "controller_name": "volume_pumper",
        "controller_type": "market_making",
        "connector_name": exchange,
        "exchange": exchange,
        "trading_pair": trading_pair,
        "order_lower_amount": order_lower_amount,
        "order_upper_amount": order_upper_amount,
        "delay_order_time": delay_order_time,
        "max_random_delay": max_random_delay,
        "balance_loss_threshold": balance_loss_threshold,
        "minimum_ask_bid_spread": minimum_ask_bid_spread,
        "periodic_report_interval": periodic_report_interval,
    }
    return config
