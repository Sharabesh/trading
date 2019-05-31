"""
This is basically a header file for all API uses.
Put global variables and API initialization terms here

Initializes control logic Alpaca,
    Setting the API key and performing initial configuration steps for the API


"""
import alpaca_trade_api as tradeapi # type: ignore
import os
from variable_typing import *

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

# Which URL is actually going to be used by application
BASE_URL = PAPER_BASE_URL

api = tradeapi.REST(KEY_ID, ALPACA_SECRET_KEY, base_url=BASE_URL)
account = api.get_account()

print(f"ACCOUNT STATUS IS {account.status}")



