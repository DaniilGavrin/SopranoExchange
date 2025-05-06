import requests
from settings import settings

# Данные для аутентификации
AUTH_LOGIN = settings.kassa_login_auth
AUTH_SECRET = settings.secter_kassa

# URL API
URL = "https://api.crystalpay.io/v3/ticker/get/"

# Тело запроса
payload = {
    "auth_login": AUTH_LOGIN,
    "auth_secret": AUTH_SECRET,
    "tickers": ["BTC", "ETH", "LTC", "SOL", "TRX", "USDT", "XMR"]
}

# Выполняем запрос
response = requests.post(URL, json=payload)

# Выводим результат
if response.status_code == 200:
    print("Список доступных валют:")
    print(response.json())
else:
    print(f"Ошибка: {response.status_code}")
    print(response.text)