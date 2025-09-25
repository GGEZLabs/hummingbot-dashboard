import copy

import nest_asyncio
import streamlit as st

from frontend.st_utils import get_backend_api_client
from frontend.utils import generate_random_name

nest_asyncio.apply()
backend_api_client = get_backend_api_client()


def get_default_config_loader(script_name: str):

    config_key = f"config_{script_name}"
    # loader_key = f"config_loader_initialized_{script_name}"

    try:
        all_configs = backend_api_client.scripts.list_script_configs()
    except Exception as e:
        st.error(f"Failed to fetch controller configs: {e}")
        all_configs = []

    existing_configs = []
    for config in all_configs:
        config_name = config.get("config_name")
        if config_name:
            existing_configs.append(config_name)
    # Create default configuration with unique ID
    default_dict = {"id": generate_random_name(existing_configs), "script_name": script_name}

    # Initialize controller-specific config if not exists
    if config_key not in st.session_state:
        st.session_state[config_key] = copy.deepcopy(default_dict)

    with st.expander("Configurations", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            use_default_config = st.checkbox(
                "Use default config",
                value=st.session_state.get(f"use_default_{script_name}", True),
                key=f"use_default_{script_name}",
            )
        with c2:
            if not use_default_config:
                # Filter configs by controller name
                configs = []
                for config in all_configs:
                    config_data = config.get("config", config)
                    if config_data.get("script_file_name").split(".")[0] == script_name:
                        configs.append(config)

                if len(configs) > 0:
                    config_names = [config.get("id") for config in configs]
                    selected_config_name = st.selectbox("Select a config", config_names, key=f"config_select_{script_name}")

                    # Find the selected config
                    selected_config = None
                    for config in configs:
                        if config.get("id") == selected_config_name:
                            selected_config = config
                            break

                    if selected_config:
                        # Use deep copy to prevent shared references
                        config_data = selected_config.get("config", selected_config)
                        st.session_state[config_key] = copy.deepcopy(config_data)
                        # Keep the original config ID
                        st.session_state[config_key]["id"] = selected_config_name
                        st.session_state[config_key]["script_name"] = script_name
                else:
                    st.warning("No existing configs found for this controller.")

    # Set legacy key for backward compatibility (but with deep copy)
    st.session_state["default_config"] = copy.deepcopy(st.session_state[config_key])


def get_script_config(script_name: str) -> dict:
    """
    Get the current configuration for a controller with proper isolation.
    Returns a deep copy to prevent shared reference mutations.
    """
    config_key = f"config_{script_name}"

    if config_key not in st.session_state:
        # Initialize with basic config if not found
        existing_configs = []
        try:
            all_configs = backend_api_client.scripts.list_script_configs()
            for config in all_configs:
                config_name = config.get("id")
                if config_name:
                    existing_configs.append(config_name.split("_")[0])
        except Exception:
            pass

        default_dict = {"id": generate_random_name(existing_configs), "script_name": script_name}
        st.session_state[config_key] = copy.deepcopy(default_dict)

    # Always return a deep copy to prevent mutations
    return copy.deepcopy(st.session_state[config_key])
