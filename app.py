import streamlit as st #web приложение
import requests
import pandas as pd
import mathplotlib.pyplot as pet

api_key = "c230b5153f2f086dca04daed705fd831"
weather = https://api.openweathermap.org/data/2.5/weather
air pollution = http://api.openweathermap.org/data/2.5/air_pollution

city = "London"
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

response = requests.get(url)
data = response.json()
print(data)
