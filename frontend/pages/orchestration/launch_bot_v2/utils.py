import time

import pandas as pd
import streamlit as st

from frontend.st_utils import get_backend_api_client

# Initialize backend client
backend_api_client = get_backend_api_client()


def launch_bot(
    bot_name,
    image_name,
    credentials,
    selected_config,
    selected_items,
    is_controller=True,
    headless_mode=True,
    max_global_drawdown=None,
    max_controller_drawdown=None,
):
    """Launch a new bot with the selected configuration."""
    if not bot_name:
        st.warning("You need to define the bot name.")
        return False
    if not image_name:
        st.warning("You need to select the hummingbot image.")
        return False
    if not selected_items:
        st.warning("You need to select at least one item. Please select an item by clicking on the checkbox or selecting a row.")
        return False

    start_time_str = time.strftime("%Y%m%d-%H%M")
    full_bot_name = f"{bot_name}-{start_time_str}"

    try:
        if is_controller:
            deploy_config = {
                "instance_name": full_bot_name,
                "credentials_profile": credentials,
                "account_config": selected_config,
                "controllers_config": [item["config_name"] for item in selected_items],
                "image": image_name,
                "headless": headless_mode,
            }
            if max_global_drawdown is not None and max_global_drawdown > 0:
                deploy_config["max_global_drawdown_quote"] = max_global_drawdown
            if max_controller_drawdown is not None and max_controller_drawdown > 0:
                deploy_config["max_controller_drawdown_quote"] = max_controller_drawdown
            backend_api_client.bot_orchestration.deploy_v2_controllers(**deploy_config)
        else:
            deploy_config = {
                "instance_name": full_bot_name,
                "credentials_profile": credentials,
                "account_config": selected_config,
                "image": image_name,
                "script": selected_items[0]["script_name"],
                "script_config": selected_items[0]["config_name"],
                "headless": headless_mode,
            }
            backend_api_client.bot_orchestration.deploy_v2_script(**deploy_config)

        st.success(f"Successfully deployed bot: {full_bot_name}")
        time.sleep(3)
        return True

    except Exception as e:
        st.error(f"Failed to deploy bot: {e}")
        return False


def delete_selected_configs(selected_configs, is_controller=True):
    """Delete selected configurations."""
    if selected_configs:
        try:
            for config in selected_configs:
                config_name = config.replace(".yml", "")
                if is_controller:
                    backend_api_client.controllers.delete_controller_config(config_name)
                else:
                    backend_api_client.scripts.delete_script_config(config_name)
                st.success(f"Deleted {config_name}")
            return True

        except Exception as e:
            st.error(f"Failed to delete configs: {e}")
            return False
    else:
        st.warning("You need to select the configs that you want to delete.")
        return False


def render_selection_ui(
    configs,
    is_controller=True,
    bot_name=None,
    image_name=None,
    credentials=None,
    selected_config=None,
    headless_mode=True,
    max_global_drawdown=None,
    max_controller_drawdown=None,
):
    """Render the selection UI for controllers or scripts."""
    strategy_type = "controller" if is_controller else "script"

    if not configs:
        st.warning(f"⚠️ No {strategy_type} configurations available. Please create some configurations first.")
        return

    st.success(f"🎛️ **{strategy_type} Selection:** Select the trading {strategy_type} you want to deploy with this bot instance")

    data = []
    for config in configs:
        if isinstance(config, str):
            st.warning(f"Unexpected config format: {config}. Expected a dictionary.")
            continue

        config_name = config.get("id")
        if not config_name:
            st.warning(f"Config missing 'id' field: {config}")
            continue

        config_data = config.get("config", config)
        connector_name = config_data.get("connector_name", "Unknown")
        trading_pair = config_data.get("trading_pair", "Unknown")

        config_parts = config_name.split("_")
        version = config_parts[-1] if len(config_parts) > 1 else "NaN"
        config_base = "_".join(config_parts[:-1]) if len(config_parts) > 1 else config_name
        # shared columns between controllers and scripts
        item_data = {
            "Config Base": config_base,
            "Version": version,
            "Connector": connector_name,
            "Trading Pair": trading_pair,
            "_config_name": config_name,
        }

        if is_controller:
            item_data["Controller Name"] = config_data.get("controller_name", config_name)
            item_data["Controller Type"] = config_data.get("controller_type", "generic")
            item_data["Amount (USDT)"] = f'${float(config_data.get("total_amount_quote", 0)):,.2f}'
        else:
            item_data["Script Name"] = config_data.get("script_name", config_name)

        data.append(item_data)

    if not data:
        return

    df = pd.DataFrame(data)
    event = st.dataframe(
        df,
        on_select="rerun",
        selection_mode="multi-row" if is_controller else "single-row",
        column_config={"_config_name": None},
        hide_index=True,
        use_container_width=True,
        key="controller_table" if is_controller else "script_table",
    )
    selected_items = []

    if is_controller:
        selected_rows = event["selection"]["rows"]
        selected_items = [{"config_name": df.iloc[row]["_config_name"]} for row in selected_rows]
    else:
        selected_rows = event["selection"]["rows"]
        selected_items = [
            {"config_name": df.iloc[row]["_config_name"],
             "script_name": df.iloc[row]["Script Name"]} for row in selected_rows
        ]

    if selected_items:
        st.success(f"✅ {len(selected_items)} {strategy_type}(s) selected for deployment")
    else:
        st.warning(f"Please select at least one {strategy_type} to deploy")

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "🗑️ Delete Selected",
            type="secondary",
            use_container_width=True,
            key=f"delete_{strategy_type}",
        ):
            if selected_items:
                if delete_selected_configs([item["config_name"] for item in selected_items], is_controller):
                    st.rerun()
            else:
                st.warning(f"Please select at least one {strategy_type} to delete")

    with col2:
        deploy_button_style = "primary" if selected_items else "secondary"
        if st.button(
            "🚀 Deploy Bot",
            type=deploy_button_style,
            use_container_width=True,
            key=f"deploy_{strategy_type}",
        ):
            if selected_items:
                with st.spinner("🚀 Starting Bot... This process may take a few seconds"):
                    if launch_bot(
                        bot_name,
                        image_name,
                        credentials,
                        selected_config,
                        selected_items,
                        is_controller,
                        headless_mode,
                        max_global_drawdown,
                        max_controller_drawdown,
                    ):
                        st.rerun()
            else:
                st.warning(f"Please select at least one {strategy_type} to deploy")
