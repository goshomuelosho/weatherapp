import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# OpenWeatherMap API Key
api_key = "c230b5153f2f086dca04daed705fd831"

# Streamlit UI
st.title("🌦️ Weather and Air Pollution Dashboard")

# Input from user
city = st.text_input("Enter city name:", "London")

# When the user inputs a city
if city:
    # Fetch current weather data
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    weather_response = requests.get(weather_url)

    if weather_response.status_code == 200:
        weather_data = weather_response.json()
        
        # Extract latitude and longitude for pollution data
        lat = weather_data["coord"]["lat"]
        lon = weather_data["coord"]["lon"]

        # Display current weather
        st.subheader(f"Weather in {city}")
        st.write(f"🌡 Temperature: {weather_data['main']['temp']} °C")
        st.write(f"☁️ Weather: {weather_data['weather'][0]['description'].title()}")
        st.write(f"💧 Humidity: {weather_data['main']['humidity']}%")
        st.write(f"💨 Wind Speed: {weather_data['wind']['speed']} m/s")

        # Fetch air pollution data
        pollution_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
        pollution_response = requests.get(pollution_url)

        if pollution_response.status_code == 200:
            pollution_data = pollution_response.json()
            components = pollution_data["list"][0]["components"]

            st.subheader("Air Pollution Data (μg/m³)")
            df = pd.DataFrame(components.items(), columns=["Pollutant", "Concentration"])
            st.dataframe(df)

            # Optional: Plot bar chart
            st.subheader("Pollution Levels")
            fig, ax = plt.subplots()
            ax.bar(df["Pollutant"], df["Concentration"], color='skyblue')
            plt.xticks(rotation=45)
            st.pyplot(fig)
        else:
            st.error("Failed to fetch air pollution data.")
    else:
        st.error("City not found or weather data unavailable.")
