from ethereum_gasprice.providers import EtherscanProvider
from httpx import Client
import config

provider = EtherscanProvider(
    secret=(config.ETHERSCAN_TOKEN),
    client=Client()
)
gas_result = provider.get_gasprice()

low = gas_result[1]['regular']
avarege = gas_result[1]['fast']
hight = gas_result[1]['fastest']