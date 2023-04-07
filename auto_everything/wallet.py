# Websites for transaction checking
# https://etherscan.io/apis
# https://bscscan.com/apis
# https://developers.tron.network/reference/get-transaction-info-by-account-address


from typing import Any


class Ethereum_Ecosystem():
    """
    It handles money traffic in ethereum ecosystem.
    For example, money in ethereum, binance network.
    """

    def __init__(self, network_url: str):
        """
        network_url: string
            Some poeple call it 'RPC URL'
            It's something like this: https://bsc-dataseed.binance.org
            You can check it in MetaMask networks settings (by adding them from https://chainlist.org) 
        """
        from web3 import Web3
        self.network_url = network_url
        self.web3 = Web3(Web3.HTTPProvider(endpoint_uri=network_url))
        print(f"Ethereum_Ecosystem network got connected: {self.web3.is_connected()}")

    def send_money(self, wallet_private_key: str, from_address: str, to_address: str, quantity: str, comments: str, gas: int) -> str | None:
        """
        wallet_private_key: string
            You can get it from MetaMask extension.
        from_address: str
        to_address: str
        quantity: str
            How many money you want to send
        comments: str
            Some message you want to deliver to others in this transaction
        gas: int
            Additional fee the server need to finish this transaction (like tax)
        """
        from web3.gas_strategies.rpc import rpc_gas_price_strategy

        try:
            self.web3.eth.set_gas_price_strategy(rpc_gas_price_strategy) #type: ignore

            tx_create = self.web3.eth.account.sign_transaction(
                {
                    "nonce": self.web3.eth.get_transaction_count(account=from_address), #type: ignore
                    "gasPrice": self.web3.eth.generate_gas_price(),
                    "gas": gas,
                    # "maxFeePerGas": self.web3.to_wei(20, "ether"),
                    # "maxPriorityFeePerGas": self.web3.to_wei(5, "ether"),
                    "to": to_address,
                    "value": self.web3.to_wei(quantity, "ether"),
                    "data": comments.encode("utf-8")
                },
                private_key=wallet_private_key
            )
            tx_hash = self.web3.eth.send_raw_transaction(tx_create.rawTransaction)
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)

            return str(tx_receipt["transactionHash"].hex())
        except Exception as e:
            print(f"error: {e}")
            return None

    # def get_transaction_history(self, from_address: str, to_address: str, comments: str, page_size: int, page_number: int) -> list[Any]:
    #     return []

    def get_transaction_detail(self, transaction_hash: str, wait: bool=False, timeout_in_seconds: int=120) -> dict[str, Any] | None:
        """
        transaction_hash: string
            You can get this hash_string when front_end make a money transferring
        wait: string
            Wait until the transaction is completed
        """
        try:
            if wait == False:
                self.web3.eth.wait_for_transaction_receipt(transaction_hash=transaction_hash, timeout=timeout_in_seconds) #type: ignore
            transaction = self.web3.eth.get_transaction(transaction_hash=transaction_hash) #type: ignore
            transaction = dict(transaction)

            if "value" in transaction:
                transaction["value"] = self._value_to_human_readble(value=transaction["value"]) #type: ignore

            return {**transaction}
        except Exception as e:
            print(f"error: {e}")
            return None

    def get_deposit(self, from_address: str) -> str:
        """
        Check how many money left in your pocket
        """
        raw_number = self.web3.eth.get_balance(from_address) #type: ignore
        return self._value_to_human_readble(value=raw_number) #type:ignore
    
    def _value_to_human_readble(self, value: str) -> str:
        return str(self.web3.from_wei(int(value), 'ether'))
    
    def _decode_input_data(self, contract_address: str, value: str) -> str:
        from web3_input_decoder import decode_constructor, decode_function #type:ignore
        import json
        import urllib.request
        f = urllib.request.urlopen(f"https://api.etherscan.io/api?module=contract&action=getabi&address={contract_address}")
        TETHER_ABI = json.loads(json.load(f)["result"])
        return decode_function(#type:ignore
            TETHER_ABI, value,#type:ignore
        )#type:ignore

if __name__ == '__main__':
    bsc_test_network_url = "https://data-seed-prebsc-1-s1.binance.org:8545"
    eth = Ethereum_Ecosystem(network_url=bsc_test_network_url)

    account_a_address = "0x1a270E5eFA5D639f5D45A2C07A12A18600EE9e22"
    account_b_address = "0x4138BcaF2DB70051261652368B0fe1c7Bf271ff4"
    private_key_for_account_a = ""

    print(eth.get_deposit(from_address=account_a_address))

    hash_string = eth.send_money(wallet_private_key=private_key_for_account_a, from_address=account_a_address, to_address=account_b_address, quantity="0.0002", comments="yingshaoxo", gas=3000000)
    print(hash_string)

    if hash_string != None:
        detail = eth.get_transaction_detail(transaction_hash=hash_string)
        print(detail)

        print(eth.get_deposit(from_address=account_a_address))

    # pprint(eth.get_transaction_detail(transaction_hash="0x8503a25ba74a1767c37af639b900c0955530b32276c6e65a08e8d13c975f6090", wait=True))
    # print(eth.get_deposit(from_address=account_a_address))

    # eth.send_money(
    #     wallet_private_key=""
    # )

    # deposit = eth.get_deposit(from_address="0x5B358fDeCC8c1C6760C7caD9D59500a5F1a180a2")
    # print(deposit)