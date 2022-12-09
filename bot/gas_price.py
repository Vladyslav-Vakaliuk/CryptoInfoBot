from ethereum_gasprice.providers import EtherscanProvider
from httpx import Client
import config as config

def gas_func():
    provider = EtherscanProvider(
        secret=(config.ETHERSCAN_TOKEN),
        client=Client()
    )
    gas_result = provider.get_gasprice()

    global low
    global avarege
    global hight

    low = gas_result[1]['regular']
    avarege = gas_result[1]['fast']
    hight = gas_result[1]['fastest']