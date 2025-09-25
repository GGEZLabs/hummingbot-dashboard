import streamlit as st

from frontend.components.save_config import render_save_config
from frontend.components.script_config_loader import get_default_config_loader

# Import submodules
from frontend.pages.config.random_transactions.user_inputs import user_inputs
from frontend.st_utils import get_backend_api_client, initialize_st_page

# Initialize the Streamlit page
initialize_st_page(title="Random Chain Transactions", icon="📈")
backend_api_client = get_backend_api_client()

# Page content
st.text("This tool will let you create a config for Random Chain Transactions and upload it to the Backend API.")
get_default_config_loader("random_transactions")

inputs, all_inputs_valid = user_inputs()

st.session_state["default_config"].update(inputs)

st.write("---")
render_save_config(
    st.session_state["default_config"]["id"], st.session_state["default_config"], all_inputs_valid, is_controller_config=False
)
