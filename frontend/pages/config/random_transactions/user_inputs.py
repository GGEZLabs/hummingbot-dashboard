from frontend.components.random_transactions_general_inputs import get_random_transactions_general_inputs


def user_inputs():
    (
        max_delay,
        min_delay,
        max_tx_amount,
        min_tx_amount,
        chain_id,
        grpc_url,
        denom,
        mnemonic_keys_with_addresses,
        all_inputs_valid,
    ) = get_random_transactions_general_inputs()

    config = {
        "min_delay": min_delay,
        "max_delay": max_delay,
        "min_tx_amount": min_tx_amount,
        "max_tx_amount": max_tx_amount,
        "chain_id": chain_id,
        "grpc_url": grpc_url,
        "denom": denom,
        "mnemonic_keys_with_addresses": mnemonic_keys_with_addresses,
        "script_file_name": "random_transactions.py",
    }
    return config, all_inputs_valid
