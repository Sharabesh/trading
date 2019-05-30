"""
Initializes control logic Alpaca,
    Setting the API key and performing initial configuration steps for the API


"""
import alpaca_trade_api as tradeapi
import os

# Initialize keys from the OS environment
try:
    KEY_ID = os.environ['ALPACA_KEY_ID']
    ALPACA_SECRET_KEY = os.environ['ALPACA_SECRET_KEY']
except:
    print("Keys not initialized in the environment please set the \"ALPACA_KEY_ID\" and \"ALPACA_SECRET_KEY\" environment variables")
    exit(-1)

