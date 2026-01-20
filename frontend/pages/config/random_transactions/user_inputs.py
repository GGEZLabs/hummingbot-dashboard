from typing import Dict, List

from frontend.components.random_transactions_general_inputs import get_random_transactions_general_inputs


def format_accounts_for_backend(chain_accounts: List[Dict[str, str]]) -> str:
    """Convert list of {key, address} dicts to 'mnemonic1:address1,mnemonic2:address2' format for encryption."""
    pairs = [f"{acc['key']}:{acc['address']}" for acc in chain_accounts]
    return ",".join(pairs)


def user_inputs():
    (
        max_delay,
        min_delay,
        max_tx_amount,
        min_tx_amount,
        chain_id,
        grpc_url,
        denom,
        chain_accounts,
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
        "mnemonic_keys_with_addresses": format_accounts_for_backend(chain_accounts),
        "script_file_name": "random_transactions.py",
    }
    return config, all_inputs_valid
