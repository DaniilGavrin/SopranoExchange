"""
    Импортируем необходимые библиотеки
"""
from decimal import Decimal
import hashlib
import requests
from crypto_pay_api_sdk import cryptopay

from settings import settings

"""
    Инициализация работы с cryptopay API
    args:
        - cryptopay ключ
        - testnet - флаг тестового режима (False - если есть не тестовая, True - если сеть тестовая)
"""
Crypto = cryptopay.Crypto("244640:AAMLyi8yUKRl1EYRHPQ3SGZMIoR5tEbXL4R", testnet = False)


def create_invoice(amount) -> tuple:
    """
    Функция для создания invoice на пополнение баланса
    args:
        - amount - сумма пополнения
    """
    result = requests.post(
        f"https://api.crystalpay.io/v3/invoice/create/", 
        json = {'auth_login': settings.kassa_login_auth, 'auth_secret': settings.secter_kassa, 'amount': amount, 'type': "purchase", 'lifetime': 1}, 
        headers = {'Content-Type': 'application/json'} 
    ).json()

    print(result)
    print(result.get('id'))
    print(result.get('url'))

    return result


def check_invoice_status(id):
    """
    Функция используется для проверки статуса платежа
    Args:
        - id платежа, берется из возврата ответа от create_invoice
    """
    result = requests.post(
        f"https://api.crystalpay.io/v3/invoice/info/", 
        json = {'auth_login': settings.kassa_login_auth, 'auth_secret': settings.secter_kassa, 'id': id}, 
        headers = {'Content-Type': 'application/json'} 
    ).json()

    print(result['state'])

    return result


def create_tron_invoice(amount, wallet):
    """
    Функция для выплаты на кошелек TRON
    Args:
        - amount - сумма платежа
        - wallet - кошелек для выплаты
    """
    try:
        method = "TRON"
        salt = settings.salt_kassa
        
        # Логирование входных данных
        print(f"\n=== Начало выполнения выплаты ===")
        print(f"Параметры:")
        print(f"Сумма: {amount}")
        print(f"Кошелек: {wallet}")
        print(f"Метод: {method}")
        print(f"SALT: {salt}")

        # Генерация подписи
        data_string = f"{amount}:{method}:{wallet}:{salt}"
        print(f"\nГенерация подписи:")
        print(f"Исходная строка: {data_string}")
        
        signature = hashlib.sha1(data_string.encode()).hexdigest()
        print(f"Подпись SHA1: {signature}")

        # Подготовка первого запроса
        payload = {
            'auth_login': settings.kassa_login_auth,
            'auth_secret': settings.secter_kassa,
            'signature': signature,
            'amount': amount,
            'method': method,
            'wallet': wallet,
            'subtract_from': "amount"
        }

        print("\nПервый запрос (создание выплаты):")
        print(f"URL: POST https://api.crystalpay.io/v3/payoff/create/")
        print("Тело запроса:")
        print(json.dumps(payload, indent=2))

        # Отправка первого запроса
        response1 = requests.post(
            "https://api.crystalpay.io/v3/payoff/create/",
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=15
        )

        print("\nОтвет первого запроса:")
        print(f"HTTP статус: {response1.status_code}")
        print(f"Ответ сервера: {response1.text}")

        # Обработка первого ответа
        try:
            result = response1.json()
        except json.JSONDecodeError:
            print("Ошибка декодирования JSON!")
            return "3"

        # Проверка первого ответа
        if result.get('error') is False or str(result.get('error')).lower() == 'false':
            print("\nУспешное создание выплаты:")
            print(json.dumps(result, indent=2))
            
            # Подготовка второго запроса
            payoff_id = result.get('id', '')
            if not payoff_id:
                print("Ошибка: отсутствует ID выплаты")
                return "3"
            
            signature_data = f"{payoff_id}:{salt}"
            print(f"\nГенерация второй подписи:")
            print(f"Исходная строка: {signature_data}")
            
            signature2 = hashlib.sha1(signature_data.encode()).hexdigest()
            print(f"Подпись SHA1: {signature2}")

            payload2 = {
                'auth_login': settings.kassa_login_auth,
                'auth_secret': settings.secter_kassa,
                'id': payoff_id,
                'signature': signature2
            }

            print("\nВторой запрос (подтверждение выплаты):")
            print(f"URL: POST https://api.crystalpay.io/v3/payoff/submit/")
            print("Тело запроса:")
            print(json.dumps(payload2, indent=2))

            # Отправка второго запроса
            response2 = requests.post(
                "https://api.crystalpay.io/v3/payoff/submit/",
                json=payload2,
                headers={'Content-Type': 'application/json'},
                timeout=15
            )

            print("\nОтвет второго запроса:")
            print(f"HTTP статус: {response2.status_code}")
            print(f"Ответ сервера: {response2.text}")

            # Обработка второго ответа
            try:
                result2 = response2.json()
            except json.JSONDecodeError:
                print("Ошибка декодирования JSON во втором ответе!")
                return "3"

            return result2

        else:
            print("\nОшибка в первом запросе:")
            print(f"Код ошибки: {result.get('code', 'неизвестен')}")
            print(f"Сообщение: {result.get('message', 'нет информации')}")
            print(f"Полный ответ: {json.dumps(result, indent=2)}")
            return "3"

    except requests.exceptions.RequestException as e:
        print(f"\nСетевая ошибка: {str(e)}")
        return "3"
    
    except Exception as e:
        print(f"\nНеожиданная ошибка: {str(e)}")
        return "3"
    
import hashlib
import requests
import json

def create_sol_invoice(amount, wallet):
    """
    Функция для выплаты на кошелек
    Args:
        - amount - сумма платежа
        - wallet - кошелек для выплаты TRON
    """
    try:
        method = "SOLANA"
        salt = settings.salt_kassa  # Убедитесь, что это правильный salt
        
        # Генерация сигнатуры
        data_string = f"{amount}:{method}:{wallet}:{salt}"
        print(f"Данные для подписи: {data_string}")
        
        signature = hashlib.sha1(data_string.encode()).hexdigest()
        print(f"Сгенерированная подпись: {signature}")

        # Первый запрос
        payload = {
            'auth_login': settings.kassa_login_auth,
            'auth_secret': settings.secter_kassa,
            'signature': signature,
            'amount': amount,
            'method': method,
            'wallet': wallet,
            'subtract_from': "amount"
        }
        
        print("\nОтправка первого запроса:")
        print(f"URL: https://api.crystalpay.io/v3/payoff/create/")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        response1 = requests.post(
            "https://api.crystalpay.io/v3/payoff/create/",
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print("\nОтвет первого запроса:")
        print(f"HTTP Status: {response1.status_code}")
        print(f"Response: {response1.text}")
        
        result = response1.json()
        
        if result.get('error') is False:
            print("\nПервый запрос успешен:")
            print(json.dumps(result, indent=2))
            
            # Подготовка второго запроса
            signature_data = f"{result['id']}:{salt}"
            print(f"\nДанные для второй подписи: {signature_data}")
            
            signature2 = hashlib.sha1(signature_data.encode()).hexdigest()
            print(f"Вторая подпись: {signature2}")
            
            payload2 = {
                'auth_login': settings.kassa_login_auth,
                'auth_secret': settings.secter_kassa,
                'id': result['id'],
                'signature': signature2
            }
            
            print("\nОтправка второго запроса:")
            print(f"URL: https://api.crystalpay.io/v3/payoff/submit/")
            print(f"Payload: {json.dumps(payload2, indent=2)}")
            
            response2 = requests.post(
                "https://api.crystalpay.io/v3/payoff/submit/",
                json=payload2,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            print("\nОтвет второго запроса:")
            print(f"HTTP Status: {response2.status_code}")
            print(f"Response: {response2.text}")
            
            result2 = response2.json()
            return result2
            
        else:
            print("\nОшибка в первом запросе:")
            print(f"Код ошибки: {result.get('code', 'неизвестен')}")
            print(f"Сообщение: {result.get('message', 'нет сообщения')}")
            return "3"
            
    except requests.exceptions.RequestException as e:
        print(f"\nОшибка сети: {str(e)}")
        return "3"
        
    except json.JSONDecodeError as e:
        print(f"\nОшибка парсинга JSON: {str(e)}")
        print(f"Сырой ответ: {response1.text if 'response1' in locals() else 'N/A'}")
        return "3"
        
    except Exception as e:
        print(f"\nНеизвестная ошибка: {str(e)}")
        return "3"
    

def create_btc_invoice(amount, wallet):
    """
    Функция для выплаты на кошелек
    Args:
        - amount - сумма платежа
        - wallet - кошелек для выплаты TRON
    """
    try:
        method = "BITCOIN"
        salt = settings.salt_kassa  # Убедитесь, что это правильный salt
        amount2 = amount
        # Генерация сигнатуры
        print(type(amount))
        data_string = f"{amount}:{method}:{wallet}:{salt}"
        print(f"Данные для подписи: {data_string}")
        
        signature = hashlib.sha1(data_string.encode()).hexdigest()
        print(f"Сгенерированная подпись: {signature}")

        # Первый запрос
        payload = {
            'auth_login': settings.kassa_login_auth,
            'auth_secret': settings.secter_kassa,
            'signature': signature,
            'amount': amount,
            'method': method,
            'wallet': wallet,
            'subtract_from': "amount"
        }
        
        print("\nОтправка первого запроса:")
        print(f"URL: https://api.crystalpay.io/v3/payoff/create/")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        response1 = requests.post(
            "https://api.crystalpay.io/v3/payoff/create/",
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print("\nОтвет первого запроса:")
        print(f"HTTP Status: {response1.status_code}")
        print(f"Response: {response1.text}")
        
        result = response1.json()
        
        if result.get('error') is False:
            print("\nПервый запрос успешен:")
            print(json.dumps(result, indent=2))
            
            # Подготовка второго запроса
            signature_data = f"{result['id']}:{salt}"
            print(f"\nДанные для второй подписи: {signature_data}")
            
            signature2 = hashlib.sha1(signature_data.encode()).hexdigest()
            print(f"Вторая подпись: {signature2}")
            
            payload2 = {
                'auth_login': settings.kassa_login_auth,
                'auth_secret': settings.secter_kassa,
                'id': result['id'],
                'signature': signature2
            }
            
            print("\nОтправка второго запроса:")
            print(f"URL: https://api.crystalpay.io/v3/payoff/submit/")
            print(f"Payload: {json.dumps(payload2, indent=2)}")
            
            response2 = requests.post(
                "https://api.crystalpay.io/v3/payoff/submit/",
                json=payload2,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            print("\nОтвет второго запроса:")
            print(f"HTTP Status: {response2.status_code}")
            print(f"Response: {response2.text}")
            
            result2 = response2.json()
            return result2
            
        else:
            print("\nОшибка в первом запросе:")
            print(f"Код ошибки: {result.get('code', 'неизвестен')}")
            print(f"Сообщение: {result.get('message', 'нет сообщения')}")
            return "3"
            
    except requests.exceptions.RequestException as e:
        print(f"\nОшибка сети: {str(e)}")
        return "3"
        
    except json.JSONDecodeError as e:
        print(f"\nОшибка парсинга JSON: {str(e)}")
        print(f"Сырой ответ: {response1.text if 'response1' in locals() else 'N/A'}")
        return "3"
        
    except Exception as e:
        print(f"\nНеизвестная ошибка: {str(e)}")
        return "3"
    
def create_eth_invoice(amount, wallet):
    """
    Функция для выплаты на кошелек
    Args:
        - amount - сумма платежа
        - wallet - кошелек для выплаты TRON
    """
    try:
        method = "ETHEREUM"
        salt = settings.salt_kassa  # Убедитесь, что это правильный salt
        
        # Генерация сигнатуры
        data_string = f"{amount}:{method}:{wallet}:{salt}"
        print(f"Данные для подписи: {data_string}")
        
        signature = hashlib.sha1(data_string.encode()).hexdigest()
        print(f"Сгенерированная подпись: {signature}")

        # Первый запрос
        payload = {
            'auth_login': settings.kassa_login_auth,
            'auth_secret': settings.secter_kassa,
            'signature': signature,
            'amount': amount,
            'method': method,
            'wallet': wallet,
            'subtract_from': "amount"
        }
        
        print("\nОтправка первого запроса:")
        print(f"URL: https://api.crystalpay.io/v3/payoff/create/")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        response1 = requests.post(
            "https://api.crystalpay.io/v3/payoff/create/",
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print("\nОтвет первого запроса:")
        print(f"HTTP Status: {response1.status_code}")
        print(f"Response: {response1.text}")
        
        result = response1.json()
        
        if result.get('error') is False:
            print("\nПервый запрос успешен:")
            print(json.dumps(result, indent=2))
            
            # Подготовка второго запроса
            signature_data = f"{result['id']}:{salt}"
            print(f"\nДанные для второй подписи: {signature_data}")
            
            signature2 = hashlib.sha1(signature_data.encode()).hexdigest()
            print(f"Вторая подпись: {signature2}")
            
            payload2 = {
                'auth_login': settings.kassa_login_auth,
                'auth_secret': settings.secter_kassa,
                'id': result['id'],
                'signature': signature2
            }
            
            print("\nОтправка второго запроса:")
            print(f"URL: https://api.crystalpay.io/v3/payoff/submit/")
            print(f"Payload: {json.dumps(payload2, indent=2)}")
            
            response2 = requests.post(
                "https://api.crystalpay.io/v3/payoff/submit/",
                json=payload2,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            print("\nОтвет второго запроса:")
            print(f"HTTP Status: {response2.status_code}")
            print(f"Response: {response2.text}")
            
            result2 = response2.json()
            return result2
            
        else:
            print("\nОшибка в первом запросе:")
            print(f"Код ошибки: {result.get('code', 'неизвестен')}")
            print(f"Сообщение: {result.get('message', 'нет сообщения')}")
            return "3"
            
    except requests.exceptions.RequestException as e:
        print(f"\nОшибка сети: {str(e)}")
        return "3"
        
    except json.JSONDecodeError as e:
        print(f"\nОшибка парсинга JSON: {str(e)}")
        print(f"Сырой ответ: {response1.text if 'response1' in locals() else 'N/A'}")
        return "3"
        
    except Exception as e:
        print(f"\nНеизвестная ошибка: {str(e)}")
        return "3"
    
def create_ltc_invoice(amount, wallet):
    """
    Функция для выплаты на кошелек
    Args:
        - amount - сумма платежа
        - wallet - кошелек для выплаты TRON
    """
    try:
        method = "LITECOIN"
        salt = settings.salt_kassa  # Убедитесь, что это правильный salt
        
        # Генерация сигнатуры
        data_string = f"{amount}:{method}:{wallet}:{salt}"
        print(f"Данные для подписи: {data_string}")
        
        signature = hashlib.sha1(data_string.encode()).hexdigest()
        print(f"Сгенерированная подпись: {signature}")

        # Первый запрос
        payload = {
            'auth_login': settings.kassa_login_auth,
            'auth_secret': settings.secter_kassa,
            'signature': signature,
            'amount': amount,
            'method': method,
            'wallet': wallet,
            'subtract_from': "amount"
        }
        
        print("\nОтправка первого запроса:")
        print(f"URL: https://api.crystalpay.io/v3/payoff/create/")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        response1 = requests.post(
            "https://api.crystalpay.io/v3/payoff/create/",
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print("\nОтвет первого запроса:")
        print(f"HTTP Status: {response1.status_code}")
        print(f"Response: {response1.text}")
        
        result = response1.json()
        
        if result.get('error') is False:
            print("\nПервый запрос успешен:")
            print(json.dumps(result, indent=2))
            
            # Подготовка второго запроса
            signature_data = f"{result['id']}:{salt}"
            print(f"\nДанные для второй подписи: {signature_data}")
            
            signature2 = hashlib.sha1(signature_data.encode()).hexdigest()
            print(f"Вторая подпись: {signature2}")
            
            payload2 = {
                'auth_login': settings.kassa_login_auth,
                'auth_secret': settings.secter_kassa,
                'id': result['id'],
                'signature': signature2
            }
            
            print("\nОтправка второго запроса:")
            print(f"URL: https://api.crystalpay.io/v3/payoff/submit/")
            print(f"Payload: {json.dumps(payload2, indent=2)}")
            
            response2 = requests.post(
                "https://api.crystalpay.io/v3/payoff/submit/",
                json=payload2,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            print("\nОтвет второго запроса:")
            print(f"HTTP Status: {response2.status_code}")
            print(f"Response: {response2.text}")
            
            result2 = response2.json()
            return result2
            
        else:
            print("\nОшибка в первом запросе:")
            print(f"Код ошибки: {result.get('code', 'неизвестен')}")
            print(f"Сообщение: {result.get('message', 'нет сообщения')}")
            return "3"
            
    except requests.exceptions.RequestException as e:
        print(f"\nОшибка сети: {str(e)}")
        return "3"
        
    except json.JSONDecodeError as e:
        print(f"\nОшибка парсинга JSON: {str(e)}")
        print(f"Сырой ответ: {response1.text if 'response1' in locals() else 'N/A'}")
        return "3"
        
    except Exception as e:
        print(f"\nНеизвестная ошибка: {str(e)}")
        return "3"
    
def create_usdt_invoice(amount, wallet):
    """
    Функция для выплаты на кошелек
    Args:
        - amount - сумма платежа
        - wallet - кошелек для выплаты TRON
    """
    try:
        method = "USDTTRC"
        salt = settings.salt_kassa  # Убедитесь, что это правильный salt
        
        # Генерация сигнатуры
        data_string = f"{amount}:{method}:{wallet}:{salt}"
        print(f"Данные для подписи: {data_string}")
        
        signature = hashlib.sha1(data_string.encode()).hexdigest()
        print(f"Сгенерированная подпись: {signature}")

        # Первый запрос
        payload = {
            'auth_login': settings.kassa_login_auth,
            'auth_secret': settings.secter_kassa,
            'signature': signature,
            'amount': str(amount),
            'method': method,
            'wallet': wallet,
            'subtract_from': "amount"
        }
        
        print("\nОтправка первого запроса:")
        print(f"URL: https://api.crystalpay.io/v3/payoff/create/")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        response1 = requests.post(
            "https://api.crystalpay.io/v3/payoff/create/",
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print("\nОтвет первого запроса:")
        print(f"HTTP Status: {response1.status_code}")
        print(f"Response: {response1.text}")
        
        result = response1.json()
        
        if result.get('error') is False:
            print("\nПервый запрос успешен:")
            print(json.dumps(result, indent=2))
            
            # Подготовка второго запроса
            signature_data = f"{result['id']}:{salt}"
            print(f"\nДанные для второй подписи: {signature_data}")
            
            signature2 = hashlib.sha1(signature_data.encode()).hexdigest()
            print(f"Вторая подпись: {signature2}")
            
            payload2 = {
                'auth_login': settings.kassa_login_auth,
                'auth_secret': settings.secter_kassa,
                'id': result['id'],
                'signature': signature2
            }
            
            print("\nОтправка второго запроса:")
            print(f"URL: https://api.crystalpay.io/v3/payoff/submit/")
            print(f"Payload: {json.dumps(payload2, indent=2)}")
            
            response2 = requests.post(
                "https://api.crystalpay.io/v3/payoff/submit/",
                json=payload2,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            print("\nОтвет второго запроса:")
            print(f"HTTP Status: {response2.status_code}")
            print(f"Response: {response2.text}")
            
            result2 = response2.json()
            return result2
            
        else:
            print("\nОшибка в первом запросе:")
            print(f"Код ошибки: {result.get('code', 'неизвестен')}")
            print(f"Сообщение: {result.get('message', 'нет сообщения')}")
            return "3"
            
    except requests.exceptions.RequestException as e:
        print(f"\nОшибка сети: {str(e)}")
        return "3"
        
    except json.JSONDecodeError as e:
        print(f"\nОшибка парсинга JSON: {str(e)}")
        print(f"Сырой ответ: {response1.text if 'response1' in locals() else 'N/A'}")
        return "3"
        
    except Exception as e:
        print(f"\nНеизвестная ошибка: {str(e)}")
        return "3"
    
def create_xmr_invoice(amount, wallet):
    """
    Функция для выплаты на кошелек
    Args:
        - amount - сумма платежа
        - wallet - кошелек для выплаты TRON
    """
    try:
        method = "USDTTRC"
        salt = settings.salt_kassa  # Убедитесь, что это правильный salt
        
        # Генерация сигнатуры
        data_string = f"{amount}:{method}:{wallet}:{salt}"
        print(f"Данные для подписи: {data_string}")
        
        signature = hashlib.sha1(data_string.encode()).hexdigest()
        print(f"Сгенерированная подпись: {signature}")

        # Первый запрос
        payload = {
            'auth_login': settings.kassa_login_auth,
            'auth_secret': settings.secter_kassa,
            'signature': signature,
            'amount': amount,
            'method': method,
            'wallet': wallet,
            'subtract_from': "amount"
        }
        
        print("\nОтправка первого запроса:")
        print(f"URL: https://api.crystalpay.io/v3/payoff/create/")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        response1 = requests.post(
            "https://api.crystalpay.io/v3/payoff/create/",
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print("\nОтвет первого запроса:")
        print(f"HTTP Status: {response1.status_code}")
        print(f"Response: {response1.text}")
        
        result = response1.json()
        
        if result.get('error') is False:
            print("\nПервый запрос успешен:")
            print(json.dumps(result, indent=2))
            
            # Подготовка второго запроса
            signature_data = f"{result['id']}:{salt}"
            print(f"\nДанные для второй подписи: {signature_data}")
            
            signature2 = hashlib.sha1(signature_data.encode()).hexdigest()
            print(f"Вторая подпись: {signature2}")
            
            payload2 = {
                'auth_login': settings.kassa_login_auth,
                'auth_secret': settings.secter_kassa,
                'id': result['id'],
                'signature': signature2
            }
            
            print("\nОтправка второго запроса:")
            print(f"URL: https://api.crystalpay.io/v3/payoff/submit/")
            print(f"Payload: {json.dumps(payload2, indent=2)}")
            
            response2 = requests.post(
                "https://api.crystalpay.io/v3/payoff/submit/",
                json=payload2,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            print("\nОтвет второго запроса:")
            print(f"HTTP Status: {response2.status_code}")
            print(f"Response: {response2.text}")
            
            result2 = response2.json()
            return result2
            
        else:
            print("\nОшибка в первом запросе:")
            print(f"Код ошибки: {result.get('code', 'неизвестен')}")
            print(f"Сообщение: {result.get('message', 'нет сообщения')}")
            return "3"
            
    except requests.exceptions.RequestException as e:
        print(f"\nОшибка сети: {str(e)}")
        return "3"
        
    except json.JSONDecodeError as e:
        print(f"\nОшибка парсинга JSON: {str(e)}")
        print(f"Сырой ответ: {response1.text if 'response1' in locals() else 'N/A'}")
        return "3"
        
    except Exception as e:
        print(f"\nНеизвестная ошибка: {str(e)}")
        return "3"