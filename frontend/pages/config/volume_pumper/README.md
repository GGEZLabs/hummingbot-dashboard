# Volume Making Strategy Configuration Tool

Welcome to the Volume Making Strategy Configuration Tool! This tool allows you to create, modify, and deploy configurations for a market volume-making strategy. Designed for flexibility and efficiency, this strategy can help you generate trading volume under defined risk parameters.

## Features

- **Start from Default Configurations**: Load default values or customize based on your previous configurations.
- **Modify Strategy Parameters**: Easily update parameters to fine-tune your volume strategy.
- **Randomized Behavior**: Built-in randomness in order timing and sizing to avoid predictability.
- **Risk Management Settings**: Limit losses with balance thresholds and spread controls.
- **Save and Reuse**: Save the final configuration for consistent deployment across sessions.

## How to Use

### 1. Load Default Configuration

Begin by loading the default configuration for the Volume Making Strategy. This serves as a starting point that you can modify according to your needs.

### 2. User Inputs

Set the configuration parameters using the input fields provided. The key configuration parameters include:

- **Exchange**: Enter the name of the exchange to trade on (e.g., `p2b`).
- **Trading Pair**: Specify the trading pair you want to trade (e.g., `GGEZ1-USDT`).
- **Order Lower Amount**: Set the minimum amount (in base asset) for any order placed (e.g., `GGEZ1`).
- **Order Upper Amount**: Set the maximum amount (in base asset) for any order placed (e.g., `GGEZ1`).
- **Delay Order Time**: Define a base delay time between placing orders.
- **Max Random Delay**: Set the upper bound of random time (in seconds) to be added to `Delay Order Time`.
- **Balance Loss Threshold**: Specify the maximum allowed balance loss (in quote currency, e.g., USDT) before halting the strategy.
- **Minimum Ask Bid Spread**: Enter the minimum acceptable ask-bid spread in basis points to ensure economic trades.
- **Periodic Report Interval**: Define how frequently (in hours) the bot should report statistics about its activity.

These settings give you precise control over how the strategy operates in terms of volume, frequency, and safety.

### 3. Save Configuration

Once you finalize the parameter settings, save the configuration using the save feature. This ensures your setup is preserved and can be quickly deployed later without re-entry.


