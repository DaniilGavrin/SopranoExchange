import requests
from settings import settings

def get_sol_rate():
    AUTH_LOGIN = settings.kassa_login_auth
    AUTH_SECRET = settings.secter_kassa
    URL = "https://api.crystalpay.io/v3/ticker/get/"
    
    payload = {
        "auth_login": AUTH_LOGIN,
        "auth_secret": AUTH_SECRET,
        "tickers": ["SOL"]
    }
    
    try:
        response = requests.post(URL, json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f'data: {data}')
            return data['currencies']['SOL']['price']
        return None
    except Exception as e:
        print(f"Ошибка при получении курса: {e}")
        return None