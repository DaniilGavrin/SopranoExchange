import requests

def rub_to_trx_rate():
    "Получение актуального курса рубля в TRX"

    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "tron",
        "vs_currencies": "rub"
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data["tron"]["rub"]