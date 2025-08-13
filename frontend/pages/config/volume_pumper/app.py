import streamlit as st

from frontend.components.config_loader import get_default_config_loader
from frontend.components.save_config import render_save_config

# Import submodules
from frontend.pages.config.volume_pumper.user_inputs import user_inputs
from frontend.st_utils import get_backend_api_client, initialize_st_page

# Initialize the Streamlit page
initialize_st_page(title="Volume Pumper", icon="📈")
backend_api_client = get_backend_api_client()

# Page content
st.text("This tool will let you create a config for Volume Pumper and upload it to the Backend API.")
get_default_config_loader("volume_pumper")

inputs = user_inputs()

st.session_state["default_config"].update(inputs)

st.write("---")
render_save_config(st.session_state["default_config"]["id"], st.session_state["default_config"])
