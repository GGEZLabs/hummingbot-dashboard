import streamlit as st

from frontend.components.config_loader import get_controller_config


def get_volume_pumper_general_inputs(custom_candles=False, controller_name: str = None):
    if controller_name:
        default_config = get_controller_config(controller_name)
    else:
        # Fallback for backward compatibility
        default_config = st.session_state.get("default_config", {})
    st.subheader("General Settings")
    with st.expander("", expanded=True):
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
    st.subheader("Volume Orders Settings")
    with st.expander("", expanded=True):

        st.text("Order Amounts")
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
        st.text("Risk Management")
        c7, c8, c9 = st.columns(3)
        balance_loss_threshold = default_config.get("balance_loss_threshold", 0)
        with c7:
            balance_loss_threshold = st.number_input(
                "maximum allowed balance loss",
                value=balance_loss_threshold,
                help=("Specify the maximum allowed balance loss (in quote currency, e.g., USDT) " "before halting the strategy."),
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
    st.subheader("Boundaries Architect Settings")
    with st.expander("", expanded=True):
        st.text("Boundaries Settings")
        c10, c11, c12, c13 = st.columns(4)
        static_support = default_config.get("static_support", 0.087)
        with c10:
            static_support = st.number_input(
                "Static Support",
                value=static_support,
                format="%.6f",
                help="Static support level price.",
            )
        static_resistance = default_config.get("static_resistance", 0.09)
        with c11:
            static_resistance = st.number_input(
                "Static Resistance",
                value=static_resistance,
                format="%.6f",
                help="Static resistance level price.",
            )
        minimum_boundaries_update_interval = default_config.get("minimum_boundaries_update_interval", 60.0)
        with c12:
            minimum_boundaries_update_interval = st.number_input(
                "Min Boundaries Update Interval",
                value=minimum_boundaries_update_interval,
                help="Minimum interval to update boundaries.",
            )
        maximum_boundaries_update_interval = default_config.get("maximum_boundaries_update_interval", 70.0)
        with c13:
            maximum_boundaries_update_interval = st.number_input(
                "Max Boundaries Update Interval",
                value=maximum_boundaries_update_interval,
                help="Maximum interval to update boundaries.",
            )

        st.text("Wall & Spread Settings")
        c14, c15, c16, c17 = st.columns(4)
        minimum_flexible_wall_spread = default_config.get("minimum_flexible_wall_spread", 0.15)
        with c14:
            minimum_flexible_wall_spread = st.number_input(
                "Min Flexible Wall Spread",
                value=minimum_flexible_wall_spread,
                format="%.4f",
                help="Minimum spread for flexible walls.",
            )
        maximum_flexible_wall_spread = default_config.get("maximum_flexible_wall_spread", 0.7)
        with c15:
            maximum_flexible_wall_spread = st.number_input(
                "Max Flexible Wall Spread",
                value=maximum_flexible_wall_spread,
                format="%.4f",
                help="Maximum spread for flexible walls.",
            )
        minimum_phase_price_change_perc = default_config.get("minimum_phase_price_change_perc", 0.01)
        with c16:
            minimum_phase_price_change_perc = st.number_input(
                "Min Phase Price Change %",
                value=minimum_phase_price_change_perc,
                format="%.4f",
                help="Minimum percentage change for phase price.",
            )
        maximum_phase_price_change_perc = default_config.get("maximum_phase_price_change_perc", 0.5)
        with c17:
            maximum_phase_price_change_perc = st.number_input(
                "Max Phase Price Change %",
                value=maximum_phase_price_change_perc,
                format="%.4f",
                help="Maximum percentage change for phase price.",
            )

        st.text("Phase & Timing Settings")
        c18, c19, c20 = st.columns(3)
        minimum_phase_period = default_config.get("minimum_phase_period", 300.0)
        with c18:
            minimum_phase_period = st.number_input(
                "Min Phase Period",
                value=minimum_phase_period,
                help="Minimum duration of a phase in seconds.",
            )
        maximum_phase_period = default_config.get("maximum_phase_period", 400.0)
        with c19:
            maximum_phase_period = st.number_input(
                "Max Phase Period",
                value=maximum_phase_period,
                help="Maximum duration of a phase in seconds.",
            )
        architect_failover_delay = default_config.get("architect_failover_delay", 10.0)
        with c20:
            architect_failover_delay = st.number_input(
                "Architect Failover Delay",
                value=architect_failover_delay,
                help="Delay for architect failover.",
            )

        st.text("Order Levels Settings")
        c21, c22 = st.columns(2)
        order_levels_steps = default_config.get("order_levels_steps", 1.0)
        with c21:
            order_levels_steps = st.number_input(
                "Order Levels Steps",
                value=order_levels_steps,
                help="Step size for order levels.",
            )
        max_allowed_depth = default_config.get("max_allowed_depth", 200)
        with c22:
            max_allowed_depth = st.number_input(
                "Max Allowed Depth",
                value=max_allowed_depth,
                help="Maximum allowed depth.",
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
        str(static_support),
        str(static_resistance),
        str(minimum_flexible_wall_spread),
        str(maximum_flexible_wall_spread),
        order_levels_steps,
        str(max_allowed_depth),
        minimum_phase_period,
        maximum_phase_period,
        str(minimum_phase_price_change_perc),
        str(maximum_phase_price_change_perc),
        minimum_boundaries_update_interval,
        maximum_boundaries_update_interval,
        architect_failover_delay,
    )
