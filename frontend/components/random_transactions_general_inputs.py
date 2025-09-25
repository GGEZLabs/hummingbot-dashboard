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
            st.session_state.chain_accounts = default_config['mnemonic_keys_with_addresses']

    with st.expander("Chain Settings", expanded=True):
        c1, c2 = st.columns(2)
        send_msg_url = default_config.get("send_msg_url", "http://108.163.148.68:8080/bank")
        with c1:
            send_msg_url = st.text_input(
                "Send message URL",
                value=send_msg_url,
                help="Enter the full send message url",
            )

        ggezchain_rest_url = default_config.get(
            "ggezchain_rest_url", "https://drest.ggez.one/cosmos/bank/v1beta1/spendable_balances"
        )
        with c2:
            ggezchain_rest_url = st.text_input(
                "GGEZ Chain Rest URL",
                value=ggezchain_rest_url,
                help="Enter the full GGEZ chain rest url",
            )

    with st.expander("Transaction Settings", expanded=True):
        c3, c4, c5, c6 = st.columns(4)

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
                "Minimum Transaction Amount", value=max_tx_amount, help="Enter the minimum transaction amount. (in uggez1)"
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
        send_msg_url,
        ggezchain_rest_url,
        st.session_state.chain_accounts,
        all_inputs_valid,
    )
