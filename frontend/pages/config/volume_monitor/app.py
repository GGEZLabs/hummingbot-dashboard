import streamlit as st

from frontend.components.save_config import render_save_config
from frontend.components.script_config_loader import get_default_config_loader
from frontend.pages.config.volume_monitor.user_inputs import user_inputs
from frontend.st_utils import initialize_st_page

# Initialize the Streamlit page
initialize_st_page(title="Volume Monitor", icon="📊", initial_sidebar_state="expanded")

st.text("This bot monitors the trading volume of a specified pair across multiple " "exchanges.")

# Load existing config or default
get_default_config_loader("volume_monitor")

# Get user inputs
inputs = user_inputs()

# Update session state with inputs
st.session_state["default_config"].update(inputs)

# Render save config section
st.write("---")
render_save_config(
    st.session_state["default_config"].get("id", "volume_monitor"),
    st.session_state["default_config"],
    True,
    is_controller_config=False,
)
