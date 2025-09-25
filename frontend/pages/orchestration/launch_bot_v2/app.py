import re

import streamlit as st

from frontend.pages.orchestration.launch_bot_v2.utils import render_selection_ui
from frontend.st_utils import get_backend_api_client, initialize_st_page

initialize_st_page(icon="🙌", show_readme=False)

# Initialize backend client
backend_api_client = get_backend_api_client()


def get_controller_configs():
    """Get all controller configurations using the new API."""
    try:
        return backend_api_client.controllers.list_controller_configs()
    except Exception as e:
        st.error(f"Failed to fetch controller configs: {e}")
        return []


def get_script_configs():
    """Get all script configurations using the new API."""
    try:
        scripts_config = backend_api_client.scripts.list_script_configs()
        return [config for config in scripts_config if config.get("script_file_name") != "v2_with_controllers.py"]
    except Exception as e:
        st.error(f"Failed to fetch script configs: {e}")
        return []


def filter_hummingbot_images(images):
    """Filter images to only show Hummingbot-related ones."""
    hummingbot_images = []
    pattern = r".+/hummingbot:"
    for image in images:
        try:
            if re.match(pattern, image):
                hummingbot_images.append(image)
        except Exception:
            continue
    return hummingbot_images


# Page Header
st.title("🚀 Deploy Trading Bot")
st.subheader("Configure and deploy your automated trading strategy")

# Bot Configuration Section
with st.container(border=True):
    st.info("🤖 **Bot Configuration:** Set up your bot instance with basic configuration")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        bot_name = st.text_input("Instance Name", placeholder="Enter a unique name for your bot instance", key="bot_name_input")
    with col2:
        try:
            available_credentials = backend_api_client.accounts.list_accounts()
            credentials = st.selectbox("Credentials Profile", options=available_credentials, index=0, key="credentials_select")
        except Exception as e:
            st.error(f"Failed to fetch credentials: {e}")
            credentials = st.text_input("Credentials Profile", value="master_account", key="credentials_input")
    with col3:
        try:
            available_configs = backend_api_client.accounts.list_accounts_configs(credentials)
            selected_config = st.selectbox("Credentials Profile configs", options=available_configs, index=0, key="config_select")
        except Exception as e:
            st.error(f"Failed to fetch credentials: {e}")
            selected_config = st.text_input("Credentials Profile configs", value="default", key="config_input")
    with col4:
        try:
            all_images = backend_api_client.docker.get_available_images("hummingbot")
            available_images = filter_hummingbot_images(all_images)
            image_name = st.selectbox("Hummingbot Image", options=available_images, index=0, key="image_select")
        except Exception as e:
            st.error(f"Failed to fetch available images: {e}")
            image_name = st.text_input("Hummingbot Image", value="hummingbot/hummingbot:latest", key="image_input")
    headless_mode = st.toggle("Run Hummingbot in Headless Mode", value=True)

# Risk Management Section
with st.container(border=True):
    st.warning("⚠️ **Risk Management:** Set maximum drawdown limits in USDT to protect your capital")
    col1, col2 = st.columns(2)
    with col1:
        max_global_drawdown = st.number_input(
            "Max Global Drawdown (USDT)",
            min_value=0.0,
            value=0.0,
            step=100.0,
            format="%.2f",
            help="Maximum allowed drawdown across all controllers",
            key="global_drawdown_input",
        )
    with col2:
        max_controller_drawdown = st.number_input(
            "Max Controller Drawdown (USDT)",
            min_value=0.0,
            value=0.0,
            step=100.0,
            format="%.2f",
            help="Maximum allowed drawdown per controller",
            key="controller_drawdown_input",
        )

# Tabs for Controllers and Scripts
tab1, tab2 = st.tabs(["🤖 Controllers", "📜 Scripts"])

with tab1:
    with st.container(border=True):
        render_selection_ui(
            configs=get_controller_configs(),
            is_controller=True,
            bot_name=bot_name,
            image_name=image_name,
            credentials=credentials,
            selected_config=selected_config,
            headless_mode=headless_mode,
            max_global_drawdown=max_global_drawdown,
            max_controller_drawdown=max_controller_drawdown,
        )

with tab2:
    with st.container(border=True):
        render_selection_ui(
            configs=get_script_configs(),
            is_controller=False,
            bot_name=bot_name,
            image_name=image_name,
            credentials=credentials,
            selected_config=selected_config,
            headless_mode=headless_mode,
        )
