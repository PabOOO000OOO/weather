import requests

API_KEY = "83c97db474822ba41aaee7adcff6ecb4"  

def get_weather(city="Moscow", units="metric"):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": units,
        "lang": "ru" 
    }
    
    try:
        response = requests.get(url, params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data.get("cod") != 200:
            print(f"Ошибка API: {data.get('message', 'Неизвестная ошибка')}")
            return None
        
        weather_info = {
            "город": data.get("name", city),
            "страна": data["sys"].get("country", "N/A"),
            "температура": data["main"].get("temp"),
            "ощущается": data["main"].get("feels_like"),
            "описание": data["weather"][0].get("description", "Нет данных"),
            "влажность": data["main"].get("humidity"),
            "ветер": data["wind"].get("speed"),
            "давление": data["main"].get("pressure")
        }
        
        return weather_info
        
    except requests.exceptions.Timeout:
        print("Ошибка: Превышен таймаут запроса (5 секунд)")
        return None
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            print("Ошибка 401: Неверный API ключ")
        elif response.status_code == 404:
            print(f"Ошибка 404: Город '{city}' не найден")
        else:
            print(f"HTTP ошибка {response.status_code}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Ошибка сети: {e}")
        return None

def main():
    city = input("Введите название города на англ (по умолчанию Moscow): ").strip()
    if not city:
        city = "Moscow"
    
    weather = get_weather(city)
    
    if not weather:
        print("Не удалось получить данные о погоде")
        return
    
    print(f"ПОГОДА В ГОРОДЕ {weather['город'].upper()}, {weather['страна']}")
    print(f"Температура: {weather['температура']}°C")
    print(f"Ощущается как: {weather['ощущается']}°C")
    print(f"Описание: {weather['описание'].capitalize()}")
    print(f"Влажность: {weather['влажность']}%")
    print(f"Ветер: {weather['ветер']} м/с")
    print(f"Давление: {weather['давление']} гПа")

if __name__ == "__main__":
    main()