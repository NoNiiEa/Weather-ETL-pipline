import json
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, UTC
from dotenv import load_dotenv
from components.temp import kevin_to_celcius
import os

if os.path.exists(".env"):
    load_dotenv(".env")
else :
    print("No .env file exit().")

city = "Bangkok,TH"
api_key = os.getenv("key")
base_url = "https://api.openweathermap.org/data/2.5/forecast"

url = f"{base_url}?q={city}&cnt=240&appid={api_key}"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    weather_data = []
    for hour in data['list']:
        date_time = datetime.fromtimestamp(hour["dt"], UTC).strftime("%Y-%m-%d %H:%M:%S")
        temp = kevin_to_celcius(hour["main"]["temp"])
        feel_like = kevin_to_celcius(hour["main"]["feels_like"])
        pressue = hour["main"]["pressure"]
        humidity = hour["main"]["humidity"]
        weather_main = hour["weather"][0]["main"]
        weather_description = hour["weather"][0]["description"]
        wind_speed = hour["wind"]["speed"]
        wind_direction = hour["wind"]["deg"]
        cloudiness = hour["clouds"]["all"]
        rain_volume = hour.get("rain", {}).get("3h", "")
        snow_volume = hour.get("snow", {}).get("3h", "")
        
        weather_data.append({
            "Datetime": date_time,
            "Temperature": temp,
            "Feels like_temp": feel_like,
            "Pressure(hPa)": pressue,
            "Humidity_percent": humidity,
            "Weather_main": weather_main,
            "Weather_description": weather_description,
            "Wind speed": wind_speed,
            "Wind direction": wind_direction,
            "Cloudiness": cloudiness,
            "Rain volume": rain_volume,
            "Snow volume": snow_volume
        })

    df = pd.DataFrame(weather_data)

    print(df.head())
else:
    print(f"Failed to get data : {response.status_code}")
