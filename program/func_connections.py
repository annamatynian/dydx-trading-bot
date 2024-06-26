""" 
from decouple import config
from dydx3 import Client
from web3 import Web3
from constants import (
    HOST,
    ETHEREUM_ADDRESS,
    DYDX_API_KEY,
    DYDX_API_SECRET,
    DYDX_API_PASSPHRASE,
    STARK_PRIVATE_KEY,
    HTTP_PROVIDER
)
#Connect to DYDX
def connect_dydx():

#Create client connection
    client = Client(
        host=HOST,
        api_key_credentials={
            "key": DYDX_API_KEY,
            "secret": DYDX_API_SECRET,
            "passphrase": DYDX_API_PASSPHRASE,
        },
        stark_private_key=STARK_PRIVATE_KEY,
        eth_private_key=config("ETH_PRIVATE_KEY"),
        default_ethereum_address=ETHEREUM_ADDRESS,
        web3=Web3(Web3.HTTPProvider(HTTP_PROVIDER))
)

#Config client
account = client.private.get_account()
account_id = account.data["account"]["id"]
quote_balance = account.data["account"]["quoteBalance"]
print("Connection successful")
print("Account ID", account_id)
print("Quote balance", quote_balance)

#Return client

""" 
import os
from dotenv import load_dotenv  
from pathlib import Path
load_dotenv()

from decouple import config
from dydx3 import Client
from web3 import Web3
from constants import (
    HOST,
    ETHEREUM_ADDRESS,
    DYDX_API_KEY,
    DYDX_API_SECRET,
    DYDX_API_PASSPHRASE,
    STARK_PRIVATE_KEY,
    HTTP_PROVIDER
)

# Dydx Helpers
HOST = "https://api.stage.dydx.exchange"


def connect_dydx():

    try:
        client = Client(
            host=HOST,
            api_key_credentials={
                "key": DYDX_API_KEY,
                "secret": DYDX_API_SECRET,
                "passphrase": DYDX_API_PASSPHRASE
            },
            stark_private_key=STARK_PRIVATE_KEY, 
            default_ethereum_address=ETHEREUM_ADDRESS,
            web3=Web3(Web3.HTTPProvider(HTTP_PROVIDER))
        )
    
        account = client.private.get_account()
        print(account)
        account_id = account.data["account"]["id"]
        quote_balance = account.data["account"]["quoteBalance"]
        print("Connection successful")
        print("Account Id", account_id)
        print("Quote balance", quote_balance)
        return client

    except Exception as e:
        print("Error:", e)
        
if __name__ == "__main__": 
    connect_dydx()