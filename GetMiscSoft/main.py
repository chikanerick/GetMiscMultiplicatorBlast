from eth_account import Account
from web3 import Web3
import json
import time

from colorama import init, Fore, Style

# Инициализируем colorama
init(autoreset=True)

def Get_wallet_adress(private_key):
    account = Account.from_key(private_key)
    address = account.address
    return address

class Wallet:
    def __init__(self, private_key):
        self.private_key = private_key
        self.addres = Get_wallet_adress(private_key)


class TxnSender:
    def __init__(self,wallet):
        self.wallet = wallet
        self.rpc_url = 'https://rpc.ankr.com/blast'

    def get_misc_multiplicator(self):
        try:
            w3 = Web3(Web3.HTTPProvider(self.rpc_url))
            nonce = w3.eth.get_transaction_count(Web3.to_checksum_address(self.wallet.addres))
            gas_price = w3.eth.gas_price

            transaction = {
                'to': Web3.to_checksum_address('0xD89dcC88AcFC6EF78Ef9602c2Bf006f0026695eF'),
                'value': Web3.to_wei(0.0000001, 'ether'),
                'gasPrice': gas_price,
                'nonce': nonce,
                'chainId':81457
            }
            estimated_gas = w3.eth.estimate_gas(transaction)
            transaction['gas'] = estimated_gas

            signed_txn = w3.eth.account.sign_transaction(transaction, self.wallet.private_key)
            txh_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            txn_receipt = w3.eth.wait_for_transaction_receipt(txh_hash)
            print(Fore.GREEN + f"({self.wallet.addres}) Получен мультипликатор MISC")
            print(f'txn Hash: {txn_receipt.transactionHash.hex()}')
            time.sleep(5)
            return True
        except Exception as e:
            print(Fore.RED + f"({self.wallet.addres}) Ошибка при получении MISC")
            print(f'Error: {e}')
            time.sleep(5)
            return False



if __name__ == "__main__":
    file = 'wallets.txt'
    
    with open(file, 'r') as f:
        data = f.readlines()
    
    keys = [line.strip() for line in data]
    total_keys = len(keys)
    
    for index, private_key in enumerate(keys, start=1):
        wallet_data = Wallet(private_key)
        txnSender = TxnSender(wallet_data)
        status_of_get_misc = txnSender.get_misc_multiplicator()  
        if status_of_get_misc == False:
            print(f'({wallet_data.addres}) Мультипликатор MISC не получен!')
            while status_of_get_misc != True:
                 status_of_get_misc = txnSender.get_misc_multiplicator()
                 time.sleep(5)
        else:
            print(f'({wallet_data.addres}) Мультипликатор MISC получен!')
            print(f'ВЫПОЛНЕНО {index} КОШЕЛЬКОВ ИЗ {total_keys}')

