# Websites for transaction checking
# https://etherscan.io/apis
# https://bscscan.com/apis
# https://developers.tron.network/reference/get-transaction-info-by-account-address


from typing import Any
from decimal import Decimal


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

    def get_transaction_detail(self, transaction_hash: str, wait: bool=False, timeout_in_seconds: int=120, only_return_value: bool = False) -> dict[str, Any] | str | None:
        """
        transaction_hash: string
            You can get this hash_string when front_end make a money transferring
        wait: string
            Wait until the transaction is completed
        only_return_value: string
        """
        try:
            if wait == False:
                self.web3.eth.wait_for_transaction_receipt(transaction_hash=transaction_hash, timeout=timeout_in_seconds) #type: ignore
            transaction = self.web3.eth.get_transaction(transaction_hash=transaction_hash) #type: ignore
            transaction = dict(transaction)

            if only_return_value == False:
                if "value" in transaction:
                    transaction["value"] = self._value_to_human_readble(value=transaction["value"]) #type: ignore
                return {**transaction}
            else:
                if "value" in transaction:
                    return self._value_to_human_readble(value=transaction["value"]) #type: ignore
                else:
                    return None
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
    
    def get_x_to_usdt_ratio(self, x: str) -> str | None:
        """
        x: string
            a token name, something like ETH, BNB, TRX and so on
        
        For example, if you set x to BNB, you may get 300 as a result, it means '1BNB == 300USDT'
        """
        import json
        import urllib.request
        try:
            raw_data_stream = urllib.request.urlopen(f"https://min-api.cryptocompare.com/data/price?fsym={x}&tsyms=USDT")
            one_x_in_usdt = json.loads(raw_data_stream.read())["USDT"]
            return one_x_in_usdt
        except Exception as e:
            print(f"error: {e}")
            return None


class Tron_Network():
    """
    It handles money traffic in tron network.
    For example, papa coin.
    """

    def __init__(self, network_url: str):
        """
        network_url: string
            Some poeple call it 'RPC URL'
            It's something like this: https://api.trongrid.io
            You can check it in here: https://developers.tron.network/docs/networks#public-network
        """
        from tronpy import Tron
        from tronpy.providers import HTTPProvider

        self.client = Tron(HTTPProvider(network_url))  # Use private network as HTTP API endpoint
    
    def get_deposit(self, from_address: str) -> str | None:
        """
        Check how many money left in your pocket
        """
        try:
            return str(self.client.get_account_balance(from_address))
        except Exception as e:
            print(f"error: {e}")
            return None
    
    def get_transaction_detail(self, transaction_hash: str, only_return_value: bool = False) -> dict[str, Any] | str | None:
        """
        transaction_hash: string
            You can get this hash_string when front_end make a money transferring
        """
        try:
            data = self.client.get_transaction(txn_id=transaction_hash) #type: ignore
            try:
                amount = str(data["raw_data"]["contract"][0]["parameter"]["value"]["amount"]) #type: ignore
                amount = str(Decimal(amount) / Decimal(1000000))
                if only_return_value == False:
                    data["raw_data"]["contract"][0]["parameter"]["value"]["amount"] = amount
                    return {**data}
                else:
                    return amount
            except Exception as e_:
                print(f"error: {e_}")
                return None
        except Exception as e:
            print(f"error: {e}")
            return None

    def send_money(self, wallet_private_key: str, from_address: str, to_address: str, quantity: str, comments: str) -> str | None:
        """
        wallet_private_key: string
            You can get it from MetaMask extension.
        from_address: str
        to_address: str
        quantity: str
            How many money you want to send
        comments: str
            Some message you want to deliver to others in this transaction
        """
        from tronpy.keys import PrivateKey

        try:
            quantity = str(Decimal(quantity)*Decimal(1000000))
            txn = (
                self.client.trx.transfer(from_address, to_address, quantity) #type: ignore
                .memo(comments) #type: ignore
                .build() #type: ignore
                .sign(PrivateKey(bytes.fromhex(wallet_private_key)))
            )
            txn.txid
            txn.broadcast().wait() #type: ignore
            return str(txn.txid)
        except Exception as e:
            print(f"error: {e}")
            return None

    def get_x_to_usdt_ratio(self, x: str) -> str | None:
        """
        x: string
            a token name, something like ETH, BNB, TRX and so on
        
        For example, if you set x to BNB, you may get 300 as a result, it means '1BNB == 300USDT'
        """
        import json
        import urllib.request
        try:
            raw_data_stream = urllib.request.urlopen(f"https://min-api.cryptocompare.com/data/price?fsym={x}&tsyms=USDT")
            one_x_in_usdt = json.loads(raw_data_stream.read())["USDT"]
            return one_x_in_usdt
        except Exception as e:
            print(f"error: {e}")
            return None


if __name__ == '__main__':
    def test_bsc():
        bsc_test_network_url = "https://data-seed-prebsc-1-s1.binance.org:8545"
        eth = Ethereum_Ecosystem(network_url=bsc_test_network_url)

        account_a_address = "0x1a270E5eFA5D639f5D45A2C07A12A18600EE9e22"
        account_b_address = "0x4138BcaF2DB70051261652368B0fe1c7Bf271ff4"
        private_key_for_account_a = "bb8fa317fe860e9bcca761342971c34bd20497c2005fe7d5eb4ae48bf40b45f9"

        # print(eth.get_deposit(from_address=account_a_address))

        # hash_string = eth.send_money(wallet_private_key=private_key_for_account_a, from_address=account_a_address, to_address=account_b_address, quantity="0.0002", comments="yingshaoxo", gas=3000000)
        # print(hash_string)

        # if hash_string != None:
        #     detail = eth.get_transaction_detail(transaction_hash=hash_string)
        #     print(detail)

        #     print(eth.get_deposit(from_address=account_a_address))

        print(eth.get_transaction_detail(transaction_hash="0x8503a25ba74a1767c37af639b900c0955530b32276c6e65a08e8d13c975f6090", wait=True))
        # print(eth.get_deposit(from_address=account_a_address))

        # eth.send_money(
        #     wallet_private_key=""
        # )

        # deposit = eth.get_deposit(from_address="0x5B358fDeCC8c1C6760C7caD9D59500a5F1a180a2")
        # print(deposit)


    tron_test_network_url = "https://api.nileex.io/"
    tron = Tron_Network(network_url=tron_test_network_url)

    account_a_address = "TXgvci3f4HUojpRJ2nmjY4TVtTNyb9ZAaE"
    account_b_address = "TPAj8fnbf59PSyn3216nuwM2H53TGsTUBH"
    private_key_for_account_a = "28f15849c4428a46810b2de78f2421e4b08e206b000431cab1fd69e35897511b"

    # print(tron.get_deposit(from_address=account_a_address))
    # print(tron.get_transaction_detail(transaction_hash="98b1b43f664de25674ea49b8ed7a57e2949990973488e4b21ff5d152d1a6f89d", only_return_value=True))
    # print(tron.send_money(private_key_for_account_a, from_address=account_a_address, to_address=account_b_address, quantity="20", comments="yingshaoxo2"))
    print(tron.get_x_to_usdt_ratio(x="trx"))