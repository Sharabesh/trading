"""
This is basically a header file for all API uses.
Put global variables and API initialization terms here

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


#Configures the BASE_URL to issue trading calls to
PAPER_BASE_URL  = "https://paper-api.alpaca.markets/"
REAL_BASE_URL =  "https://api.alpaca.markets/"



api = tradeapi.REST(KEY_ID, ALPACA_SECRET_KEY, base_url=PAPER_BASE_URL)
account = api.get_account()

print(f"ACCOUNT STATUS IS {account.status}")



