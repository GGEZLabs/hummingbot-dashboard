# Volume Monitor

This bot monitors the trading volume of a specified pair across multiple exchanges.
At regular `refresh_time` intervals, it checks the current volume against a `volume_threshold`.
If the volume is below the threshold, a notification is sent to the user via Telegram.
If the volume is above the threshold, a log message is printed.
The bot is designed to be API-efficient, remaining idle for most of the time between checks.
