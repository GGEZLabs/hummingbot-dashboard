import streamlit as st
from frontend.components.config_loader import get_controller_config


def get_volume_pumper_general_inputs(custom_candles=False, controller_name: str = None):
    if controller_name:
        default_config = get_controller_config(controller_name)
    else:
        # Fallback for backward compatibility
        default_config = st.session_state.get("default_config", {})
    with st.expander("General Settings", expanded=True):
        c1, c2 = st.columns(2)

        exchange = default_config.get("exchange", "p2b")
        with c1:
            exchange = st.text_input(
                "Connector", value=exchange, help="Enter the name of the exchange to trade on (e.g., `p2b`)."
            )

        trading_pair = default_config.get("trading_pair", "GGEZ1-USDT")
        with c2:
            trading_pair = st.text_input(
                "Trading Pair", value=trading_pair, help="Enter the trading pair to trade on (e.g., GGEZ1-USDT)."
            )

    with st.expander("Order Amounts Settings", expanded=True):
        c3, c4, c5, c6 = st.columns(4)
        order_lower_amount = default_config.get("order_lower_amount", 20)
        with c3:
            order_lower_amount = st.number_input(
                "Minimum Order Amount (in base asset)",
                value=order_lower_amount,
                help="Set the minimum amount (in base asset) for any order placed (e.g., `GGEZ1`).",
            )
        order_upper_amount = default_config.get("order_upper_amount", 100)
        with c4:
            order_upper_amount = st.number_input(
                "Maximum Order Amount (in base asset)",
                value=order_upper_amount,
                help="Set the maximum amount (in base asset) for any order placed (e.g., `GGEZ1`).",
            )
        delay_order_time = default_config.get("delay_order_time", 30)
        with c5:
            delay_order_time = st.number_input(
                "Between Orders Base Delay",
                value=delay_order_time,
                help="Define a base delay time between placing orders. (in seconds)",
            )
        max_random_delay = default_config.get("max_random_delay", 30)
        with c6:
            max_random_delay = st.number_input(
                "Between Orders Random Delay",
                value=max_random_delay,
                help="Set the upper bound of random time (in seconds) to be added to `Delay Order Time`.",
            )
    with st.expander("Risk Management Settings", expanded=True):
        c7, c8, c9 = st.columns(3)
        balance_loss_threshold = default_config.get("balance_loss_threshold", 0)
        with c7:
            balance_loss_threshold = st.number_input(
                "maximum allowed balance loss",
                value=balance_loss_threshold,
                help="Specify the maximum allowed balance loss (in quote currency, e.g., USDT) before halting the strategy.",
            )
        minimum_ask_bid_spread = default_config.get("minimum_ask_bid_spread", 1)
        with c8:
            minimum_ask_bid_spread = st.number_input(
                "minimum acceptable ask-bid spread (in basis points) ",
                value=minimum_ask_bid_spread,
                help="Enter the minimum acceptable ask-bid spread in basis points to ensure economic trades.",
            )
        periodic_report_interval = default_config.get("periodic_report_interval", 1)
        with c9:
            periodic_report_interval = st.number_input(
                "Periodic Report Interval",
                value=periodic_report_interval,
                help="Define how frequently (in hours) the bot should report statistics about its activity.",
            )

    return (
        exchange,
        trading_pair,
        order_lower_amount,
        order_upper_amount,
        delay_order_time,
        max_random_delay,
        balance_loss_threshold,
        minimum_ask_bid_spread,
        periodic_report_interval,
    )
