from frontend.components.volume_pumper_general_inputs import get_volume_pumper_general_inputs


def user_inputs():
    # default_config = st.session_state.get("default_config", {})
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
        static_support,
        static_resistance,
        minimum_flexible_wall_spread,
        maximum_flexible_wall_spread,
        order_levels_steps,
        max_allowed_depth,
        minimum_phase_period,
        maximum_phase_period,
        minimum_phase_price_change_perc,
        maximum_phase_price_change_perc,
        minimum_boundaries_update_interval,
        maximum_boundaries_update_interval,
        architect_failover_delay,
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
        "static_support": static_support,
        "static_resistance": static_resistance,
        "minimum_flexible_wall_spread": minimum_flexible_wall_spread,
        "maximum_flexible_wall_spread": maximum_flexible_wall_spread,
        "order_levels_steps": order_levels_steps,
        "max_allowed_depth": max_allowed_depth,
        "minimum_phase_period": minimum_phase_period,
        "maximum_phase_period": maximum_phase_period,
        "minimum_phase_price_change_perc": minimum_phase_price_change_perc,
        "maximum_phase_price_change_perc": maximum_phase_price_change_perc,
        "minimum_boundaries_update_interval": minimum_boundaries_update_interval,
        "maximum_boundaries_update_interval": maximum_boundaries_update_interval,
        "architect_failover_delay": architect_failover_delay,
    }
    return config
