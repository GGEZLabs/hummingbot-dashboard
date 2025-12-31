import re

import streamlit as st

from frontend.components.script_config_loader import get_script_config


def get_random_transactions_general_inputs(custom_candles=False, script_name: str = None):
    if script_name:
        default_config = get_script_config(script_name)
    else:
        # Fallback for backward compatibility
        default_config = st.session_state.get("default_config", {})
        if "mnemonic_keys_with_addresses" in default_config:
            st.session_state.chain_accounts = default_config["mnemonic_keys_with_addresses"]

    with st.expander("Chain Settings", expanded=True):
        c1, c2 = st.columns(2)
        chain_id = default_config.get("chain_id", "ggezchain")
        with c1:
            chain_id = st.text_input(
                "Chain ID",
                value=chain_id,
                help="Enter the chain id",
            )

        grpc_url = default_config.get("grpc_url", "172.21.10.116:9090")
        with c2:
            grpc_url = st.text_input(
                "GRPC URL",
                value=grpc_url,
                help="Enter the full GRPC url",
            )

    with st.expander("Transaction Settings", expanded=True):
        c3, c4 = st.columns(2)
        c5, c6, c7 = st.columns(3)

        min_delay = default_config.get("min_delay", 60)
        with c3:
            min_delay = st.number_input(
                "Minimum Transaction Delay", value=min_delay, help="Enter the minimum transaction delay. (in seconds)"
            )

        max_delay = default_config.get("max_delay", 900)
        with c4:
            max_delay = st.number_input(
                "Maximum Transaction Delay", value=max_delay, help="Enter the maximum transaction delay. (in seconds)"
            )

        min_tx_amount = default_config.get("min_tx_amount", 1000000)
        with c5:
            min_tx_amount = st.number_input(
                "Minimum Transaction Amount", value=min_tx_amount, help="Enter the minimum transaction amount. (in uggez1)"
            )

        max_tx_amount = default_config.get("max_tx_amount", 3000000)
        with c6:
            max_tx_amount = st.number_input(
                "Maximum Transaction Amount", value=max_tx_amount, help="Enter the maximum transaction amount. (in uggez1)"
            )

        denom = default_config.get("denom", "uggez1")
        with c7:
            denom = st.text_input(
                "Denom",
                value=denom,
                help="Enter the denom",
            )

    with st.expander("Accounts Settings", expanded=True):
        MNEMONIC_REGEX = r"^((\w+\s){11}|(\w+\s){23})\w+$"
        ADDRESS_REGEX = r"^ggez[A-Za-z0-9]{30,80}$"
        minimum_num_of_accounts = 2

        # --- Initialize Session State ---
        if "chain_accounts" not in st.session_state:
            st.session_state.chain_accounts = [{"key": "", "address": ""}, {"key": "", "address": ""}]

        all_inputs_valid = True
        # --- Top-Level "Add" Button ---
        if st.button("➕ Add New Account"):
            st.session_state.chain_accounts.append({"key": "", "address": ""})
            st.rerun()

        all_inputs_valid = True

        for i in range(len(st.session_state.chain_accounts) - 1, -1, -1):
            account = st.session_state.chain_accounts[i]

            c1, c2, c3 = st.columns([5, 5, 1])
            with c1:
                key_value = st.text_input(f"Mnemonic Key {i + 1}", value=account["key"], key=f"key_{i}")
                st.session_state.chain_accounts[i]["key"] = key_value

                if not re.fullmatch(MNEMONIC_REGEX, key_value.strip()):
                    st.error("Invalid format: Must be a 12 or 24-word phrase.", icon="🚨")
                    all_inputs_valid = False

            with c2:
                address_value = st.text_input(f"Address {i + 1}", value=account["address"], key=f"address_{i}")
                st.session_state.chain_accounts[i]["address"] = address_value

                if not re.fullmatch(ADDRESS_REGEX, address_value.strip()):
                    st.error("Invalid format: Must start with 'ggez'.", icon="🚨")
                    all_inputs_valid = False

            with c3:
                # Add a placeholder to vertically align the button
                st.write("")
                st.write("")
                if st.button("🗑️", key=f"remove_{i}"):
                    if len(st.session_state.chain_accounts) > minimum_num_of_accounts:
                        st.session_state.chain_accounts.pop(i)
                        st.rerun()
                    else:
                        st.toast(f"Minimum of {minimum_num_of_accounts} accounts required.")

        # Display the validation status and the stored data
        if all_inputs_valid:
            st.success("All account formats are valid!")
        else:
            st.warning("Please correct the invalid fields above.")
        st.text("Current Accounts Data:")
        st.json(body=st.session_state.chain_accounts, expanded=False)
    # mnemonic_keys_with_addresses = st.session_state.chain_accounts
    return (
        max_delay,
        min_delay,
        max_tx_amount,
        min_tx_amount,
        chain_id,
        grpc_url,
        denom,
        st.session_state.chain_accounts,
        all_inputs_valid,
    )
