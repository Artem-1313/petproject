import requests


def wheather_API():
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=175e5c7d4d8e320e7d84aa05932b4bb8'
    cities = ['Barcelona', 'London', 'Kyiv']
    tmp = []
    for city in cities:
        # convert F to Celcium
        def F_C(grad):
            return f"{round((5 / 9) * (grad - 32), 2)} C"

        city_weather = requests.get(
            url.format(city)).json()  # request the API data and convert the JSON to Python data types

        city_temperature = {
            'city': city,
            "current_temperature": F_C(city_weather['main']['temp']),
            "max_temperature": F_C(city_weather['main']['temp_max']),
            "min_temperature": F_C(city_weather['main']['temp_min']),
            "icon": city_weather['weather'][0]['icon']
        }
        tmp.append(city_temperature)
    return tmp


get_wheather=wheather_API()