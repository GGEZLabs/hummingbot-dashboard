import json

import nest_asyncio
import streamlit as st

from frontend.st_utils import get_backend_api_client, initialize_st_page

nest_asyncio.apply()

initialize_st_page(title="Credentials", icon="🔑")

# Page content
client = get_backend_api_client()
NUM_COLUMNS = 4


def get_all_connectors_config_map():
    # Get fresh client instance inside cached function
    connectors = client.connectors.list_connectors()
    config_map_dict = {}
    for connector_name in connectors:
        try:
            config_map = client.connectors.get_config_map(connector_name=connector_name)
            config_map_dict[connector_name] = config_map
        except Exception as e:
            st.warning(f"Could not get config map for {connector_name}: {e}")
            config_map_dict[connector_name] = []
    return config_map_dict


all_connector_config_map = get_all_connectors_config_map()


@st.fragment
def accounts_section():
    # Get fresh accounts list
    accounts = client.accounts.list_accounts()

    if accounts:
        n_accounts = len(accounts)
        # Ensure master_account is first, but handle if it doesn't exist
        if "master_account" in accounts:
            accounts.remove("master_account")
            accounts.insert(0, "master_account")
        for i in range(0, n_accounts, NUM_COLUMNS):
            cols = st.columns(NUM_COLUMNS)
            for j, account in enumerate(accounts[i: i + NUM_COLUMNS]):
                with cols[j]:
                    st.subheader(f"🏦  {account}")
                    credentials = client.accounts.list_account_credentials(account)
                    st.json(credentials)
    else:
        st.write("No accounts available.")

    st.markdown("---")

    # Account management actions
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        # Section to create a new account
        st.header("Create a New Account")
        new_account_name = st.text_input("New Account Name")
        if st.button("Create Account"):
            new_account_name = new_account_name.replace(" ", "_")
            if new_account_name:
                if new_account_name in accounts:
                    st.warning(f"Account {new_account_name} already exists.")
                    st.stop()
                elif new_account_name == "" or all(char == "_" for char in new_account_name):
                    st.warning("Please enter a valid account name.")
                    st.stop()
                response = client.accounts.add_account(new_account_name)
                st.write(response)
                try:
                    st.rerun(scope="fragment")
                except Exception:
                    st.rerun()
            else:
                st.write("Please enter an account name.")

    with c2:
        # Section to delete an existing account
        st.header("Delete an Account")
        delete_account_name = st.selectbox(
            "Select Account to Delete",
            options=accounts if accounts else ["No accounts available"],
        )
        if st.button("Delete Account"):
            if delete_account_name and delete_account_name != "No accounts available":
                response = client.accounts.delete_account(delete_account_name)
                st.warning(response)
                try:
                    st.rerun(scope="fragment")
                except Exception:
                    st.rerun()
            else:
                st.write("Please select a valid account.")

    with c3:
        # Section to delete a credential from an existing account
        st.header("Delete Credential")
        delete_account_cred_name = st.selectbox(
            "Select the credentials account",
            options=accounts if accounts else ["No accounts available"],
        )
        credentials_data = client.accounts.list_account_credentials(delete_account_cred_name)
        # Handle different possible return formats
        if isinstance(credentials_data, list):
            # If it's a list of strings in format "connector.key"
            if credentials_data and isinstance(credentials_data[0], str):
                creds_for_account = [credential.split(".")[0] for credential in credentials_data]
            # If it's a list of dicts, extract connector names
            elif credentials_data and isinstance(credentials_data[0], dict):
                creds_for_account = list(
                    set(
                        [
                            cred.get("connector", cred.get("connector_name", ""))
                            for cred in credentials_data
                            if cred.get("connector") or cred.get("connector_name")
                        ]
                    )
                )
            else:
                creds_for_account = []
        elif isinstance(credentials_data, dict):
            # If it's a dict with connectors as keys
            creds_for_account = list(credentials_data.keys())
        else:
            creds_for_account = []
        delete_cred_name = st.selectbox(
            "Select a Credential to Delete", options=creds_for_account if creds_for_account else ["No credentials available"]
        )
        if st.button("Delete Credential"):
            if (delete_account_cred_name and delete_account_cred_name != "No accounts available") and (
                delete_cred_name and delete_cred_name != "No credentials available"
            ):
                response = client.accounts.delete_credential(delete_account_cred_name, delete_cred_name)
                st.warning(response)
                try:
                    st.rerun(scope="fragment")
                except Exception:
                    st.rerun()
            else:
                st.write("Please select a valid account.")

    return accounts


accounts = accounts_section()

st.markdown("---")


# Section to add credentials
@st.fragment
def add_credentials_section():
    st.header("Add Credentials")
    c1, c2 = st.columns([1, 1])
    with c1:
        account_name = st.selectbox("Select Account", options=accounts if accounts else ["No accounts available"])
    with c2:
        all_connectors = list(all_connector_config_map.keys())
        binance_perpetual_index = all_connectors.index("binance_perpetual") if "binance_perpetual" in all_connectors else None
        connector_name = st.selectbox("Select Connector", options=all_connectors, index=binance_perpetual_index)
        config_map = all_connector_config_map.get(connector_name, [])

    st.write(f"Configuration Map for {connector_name}:")
    config_inputs = {}

    # Custom logic for XRPL connector
    if connector_name == "xrpl":
        # Define custom XRPL fields with default values
        xrpl_fields = {
            "xrpl_secret_key": "",
            "wss_node_urls": "wss://xrplcluster.com,wss://s1.ripple.com,wss://s2.ripple.com",
        }

        # Display XRPL-specific fields
        for field, default_value in xrpl_fields.items():
            if field == "xrpl_secret_key":
                config_inputs[field] = st.text_input(field, type="password", key=f"{connector_name}_{field}")
            else:
                config_inputs[field] = st.text_input(field, value=default_value, key=f"{connector_name}_{field}")

        if st.button("Submit Credentials"):
            response = client.accounts.add_credential(account_name, connector_name, config_inputs)
            if response:
                st.success(response)
                try:
                    st.rerun(scope="fragment")
                except Exception:
                    st.rerun()
    else:
        # Default behavior for other connectors
        cols = st.columns(NUM_COLUMNS)
        for i, config in enumerate(config_map):
            with cols[i % (NUM_COLUMNS - 1)]:
                config_inputs[config] = st.text_input(config, type="password", key=f"{connector_name}_{config}")

        with cols[-1]:
            if st.button("Submit Credentials"):
                response = client.accounts.add_credential(account_name, connector_name, config_inputs)
                if response:
                    st.success(response)
                    try:
                        st.rerun(scope="fragment")
                    except Exception:
                        st.rerun()


add_credentials_section()


@st.cache_data(ttl=600)
def get_accounts(_client):
    """Fetches and caches the list of accounts."""
    print("DEBUG: Fetching fresh list of accounts from API.")
    accounts = _client.accounts.list_accounts()
    if "master_account" in accounts:
        accounts.remove("master_account")
        accounts.insert(0, "master_account")
    return accounts


@st.cache_data(ttl=600)
def get_account_configs(_client, account_name):
    """Fetches and caches the configs for a specific account."""
    if not account_name or account_name == "No accounts available":
        return []
    print(f"DEBUG: Fetching fresh configs for {account_name} from API.")
    return _client.accounts.list_accounts_configs(account_name)


@st.cache_data(ttl=600)
def get_config_details(_client, account_name, config_name):
    """Fetches and caches the details of a specific config."""
    print(f"DEBUG: Fetching fresh details for {config_name} in {account_name}.")
    return _client.accounts.get_account_config(account_name, config_name)


def render_add_config_ui(client, accounts):
    """UI section for adding a new configuration."""
    st.header("➕ Add New Config")
    if not accounts:
        st.info("No accounts available to add configs to.")
        return

    account_name = st.selectbox("Select Account", options=accounts, key="add_config_account_select")

    new_config_name = st.text_input("New Config Name", key="new_config_name_input")

    if st.button("Create New Config"):
        clean_config_name = new_config_name.strip().replace(" ", "_")

        if not clean_config_name or all(c == "_" for c in clean_config_name):
            st.warning("Please enter a valid configuration name.")
        else:
            try:
                client.accounts.add_account_config(account_name, clean_config_name)
                st.success(f"Successfully created config '{clean_config_name}'!")
                get_account_configs.clear(client, account_name)
                st.rerun()
            except Exception as e:
                st.error(f"Config '{clean_config_name}' may already exist or another error occurred: {e}")


@st.dialog("Configuration Details", width="large")
def show_config_popup(config):
    st.info("Top-level items are shown. Click to expand nested objects.", icon="👇")
    st.json(config, expanded=False)
    if st.button("Close"):
        st.rerun()


README_DOC = """
# 📘 Hummingbot Configuration Help

This popup allows you to update keys in the config. Below are explanations
 and recommended values for important sections.

---

### 🔹 market_data_collection
- **market_data_collection_enabled**
  *Description*: Enable/disable the Market Data Collection feature.
  *Recommended*: `true`

- **market_data_collection_interval**
  *Description*: Market data collection interval (in seconds).
  *Recommended*: `60`

- **market_data_collection_depth**
  *Description*: Order book collection depth.
  *Recommended*: `2`

---

### 🔹 rate_oracle_source
- **name**
  *Description*: The exchange source to pull token price data from.
  *Recommended*: `p2b`, `uzx`, or `coinstore`.
  *Note*: For **"GGEZ1"** Token only available with **p2b**, **uzx**, or
    **coinstore**. Use the same exchange as in your running strategy.

---

### 🔹 certs_path
- *Description*: Path to the `certs` folder.
- *Recommended*:
  - **Docker** → `/home/hummingbot/certs`
  - **Source install** → actual path to your `certs` folder

---

### 🔹 db_mode
The database used to store orders, controller state, and market data.

**Configuration Parameters:**
- **db_engine** → one of: `sqlite`, `postgresql`, `mysql`, `oracle`, `mssql`
- **db_host** → e.g. `127.0.0.1`
- **db_port** → e.g. `3306`
- **db_username** → database username
- **db_password** → database password
- **db_name** → database name
- **db_schema** (Postgres only) → schema name, e.g. `market`

---

### 🔹 telegram_mode (HBot ≥ v2.2)
Enable Telegram bot integration to control Hummingbot from Telegram.

Steps:
1. Create a Telegram bot.
2. Add it to a group chat or start a private chat.
3. Get the bot token and chat ID.

📖 See docs: [Telegram Setup](https://hummingbot.org/global-configs/telegram/)

**Configuration Parameters:**
- **telegram_token** → Bot token string
- **telegram_chat_id** → Chat ID to receive messages

---
"""


@st.dialog("Update Configuration Details", width="large")
def update_config_popup(config, account_name: str, config_name: str):
    st.info("Update the fields below and click Save.", icon="✏️")
    with st.expander("📘 README / Config Reference", expanded=False):
        st.markdown(README_DOC)
    edited_json = st.text_area(
        "Edit Config (JSON)",
        value=json.dumps(config, indent=2),
        height=400,
        key="update_config_text_area",
    )
    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("Save Changes ✅"):
            try:
                new_config = json.loads(edited_json)
                response = client.accounts.update_account_config(account_name, config_name, new_config)
                st.success(f"Successfully updated '{response}'.")
                get_config_details.clear(client, account_name, config_name)
            except json.JSONDecodeError as e:
                st.error(f"Invalid JSON: {e}")
            except Exception as e:
                st.error(f"Could not update config: {e}")
    with c2:
        if st.button("Cancel ❌"):
            st.rerun()


def render_manage_configs_ui(client, accounts):
    """A consolidated UI for viewing, updating, and deleting existing configs."""
    st.header("⚙️ Manage Existing Configs")

    if not accounts:
        st.info("No accounts available to manage.")
        return

    account_name = st.selectbox("Select an account to manage its configs", options=accounts, key="manage_configs_account_select")

    account_configs = get_account_configs(client, account_name)

    if not account_configs:
        st.info(f"Account '{account_name}' has no configurations.")
        return

    st.write("---")

    for config_name in account_configs:
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        with col1:
            st.markdown(f"📄 **{config_name}**")
        with col2:
            if st.button("View", key=f"view_{account_name}_{config_name}", use_container_width=True):
                try:
                    config_data = get_config_details(client, account_name, config_name)
                    show_config_popup(config_data.get("client_config", {}))
                except Exception as e:
                    st.error(f"Could not load '{config_name}': {e}")
        with col3:
            if st.button("Update", key=f"update_{account_name}_{config_name}", use_container_width=True):
                try:
                    config_data = get_config_details(client, account_name, config_name)
                    update_config_popup(config_data.get("client_config", {}), account_name, config_name)
                except Exception as e:
                    st.error(f"Could not load '{config_name}': {e}")
        with col4:
            is_default = config_name == "default"
            if st.button(
                "Delete",
                key=f"delete_{account_name}_{config_name}",
                type="primary",
                disabled=is_default,
                use_container_width=True,
            ):
                try:
                    client.accounts.delete_account_config(account_name, config_name)
                    st.success(f"Successfully deleted config '{config_name}'.")
                    get_account_configs.clear(client, account_name)
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to delete config: {e}")


def accounts_configs_page():
    """Main function to render the entire accounts configuration page."""
    st.markdown("---")
    st.header("Accounts Configuration Management")
    st.info("Add new configurations or manage existing ones for any account.")

    accounts = get_accounts(client)

    add_col, manage_col = st.columns(2, gap="large")

    with add_col:
        render_add_config_ui(client, accounts)

    with manage_col:
        render_manage_configs_ui(client, accounts)


accounts_configs_page()
