"""
This is basically a header file for all API uses.
Put global variables and API initialization terms here

Initializes control logic Alpaca,
    Setting the API key and performing initial configuration steps for the API


"""
import alpaca_trade_api as tradeapi # type: ignore
import os

# Initialize keys from the OS environment
try:
    PAPER_KEY_ID = os.environ['PAPER_ALPACA_KEY_ID']
    PAPER_ALPACA_SECRET_KEY = os.environ['PAPER_ALPACA_SECRET_KEY']
    KEY_ID = os.environ['ALPACA_KEY_ID']
    ALPACA_SECRET_KEY = os.environ['ALPACA_SECRET_KEY']
    # PAPER_ID = os.environ['ALPACA_PAPER_ID']
    # PAPER_SECRET = os.environ['ALPACA_PAPER_SECRET']
except:
    print("Keys not initialized in the environment please set the \"ALPACA_KEY_ID\" and \"ALPACA_SECRET_KEY\" environment variables")
    exit(-1)



#Configures the BASE_URL to issue trading calls to
PAPER_BASE_URL  = "https://paper-api.alpaca.markets"
REAL_BASE_URL =  "https://api.alpaca.markets"

# Which URL is actually going to be used by application
BASE_URL = PAPER_BASE_URL # For now limit to paper trading

# api = tradeapi.REST(KEY_ID if BASE_URL == REAL_BASE_URL else PAPER_ID,
#                    ALPACA_SECRET_KEY if BASE_URL == REAL_BASE_URL else PAPER_SECRET,
#                    base_url=BASE_URL)

if BASE_URL == REAL_BASE_URL:
    api = tradeapi.REST(KEY_ID, ALPACA_SECRET_KEY, BASE_URL)
else:
    api = tradeapi.REST(PAPER_KEY_ID, PAPER_ALPACA_SECRET_KEY, PAPER_BASE_URL)


account = api.get_account()

print(f"ACCOUNT STATUS IS {account.status}")



