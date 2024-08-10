import hashlib
import requests
from settings import *
import settings
from crypto_pay_api_sdk import cryptopay

Crypto = cryptopay.Crypto("244640:AAMLyi8yUKRl1EYRHPQ3SGZMIoR5tEbXL4R", testnet = False)

def create_invoice(amount) -> tuple:
    result = requests.post(
        f"https://api.crystalpay.io/v2/invoice/create/", 
        json = {'auth_login': "testikkassa", 'auth_secret': "aba713300137e12ee1737b9bf9603ce160a5c5db", 'amount': amount, 'type': "purchase", 'lifetime': 1}, 
        headers = {'Content-Type': 'application/json'} 
    ).json()

    print(result)
    print(result.get('id'))
    print(result.get('url'))

    return result


def check_invoice_status(id):
    result = requests.post(
        f"https://api.crystalpay.io/v2/invoice/info/", 
        json = {'auth_login': "testikkassa", 'auth_secret': "aba713300137e12ee1737b9bf9603ce160a5c5db", 'id': id}, 
        headers = {'Content-Type': 'application/json'} 
    ).json()

    print(result['state'])

    return result


def create_tron_invoice(amount, wallet):
    method = "TRON"
    wallet = "TTR7972728515748602593"  # Троновая кошелка для выплаты
    salt = settings.salt_kassa
    signature = hashlib.sha1(str.encode(f"{amount}:{method}:{wallet}:{salt}")).hexdigest()
    print(signature)
    print(f"{amount}:{method}:{wallet}:{salt}")
    result = requests.post(
        f"https://api.crystalpay.io/v2/payoff/create/",
        json = {'auth_login': "testikkassa", 'auth_secret': "aba713300137e12ee1737b9bf9603ce160a5c5db", 'signature': signature, 'amount': amount, 'method': method, 'wallet': wallet, 'subtract_from': "amount"},
        headers = {'Content-Type': 'application/json'}
    ).json()
    if result.get('error') == 'False':
        signature2 = hashlib.sha1(str.encode(f"{result['id']}:{salt}")).hexdigest()
        result2 = requests.post(
            f"https://api.crystalpay.io/v2/payoff/submit/",
            json = {'auth_login': "testikkassa", 'auth_secret': "aba713300137e12ee1737b9bf9603ce160a5c5db", 'id': result['id'], "signature": signature2},
            headers = {'Content-Type': 'application/json'}
        ).json()

        return result2
    else:
        return "3"