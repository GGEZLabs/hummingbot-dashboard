# Random Transactions Strategy

## Use Case

The Random Transactions strategy is designed to automate the process of sending random transactions between a set of predefined accounts. This simulates user activity.

The core functionality of this strategy is to:

- Send transactions of `uggez1` coins.
- Send transactions between a list of provided accounts.
- Randomize the amount of coins sent in each transaction within a defined range.
- Randomize the time interval between each transaction within a defined range.

## Configuration

Here is a breakdown of the configuration parameters for this strategy:

| Parameter | Description |
| --- | --- |
| `min_delay` | The minimum time in seconds to wait before sending the next transaction. |
| `max_delay` | The maximum time in seconds to wait before sending the next transaction. The actual delay will be a random value between `min_delay` and `max_delay`. |
| `min_tx_amount` | The minimum amount of `uggez1` coins to send in a single transaction. |
| `max_tx_amount` | The maximum amount of `uggez1` coins to send in a single transaction. The actual amount will be a random value between `min_tx_amount` and `max_tx_amount`. |
| `send_msg_url` | The URL endpoint responsible for processing the transaction message. |
| `ggezchain_rest_url` | The REST URL of the ggezchain network. |
| `mnemonic_keys_with_addresses` | A list of mnemonic keys and their corresponding addresses that will be used to send and receive the transactions. |
| `script_file_name` | The name of the script file to be executed. For this strategy, it should be `random_transactions.py`. |