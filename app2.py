import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# OpenWeatherMap API Key
api_key = "c230b5153f2f086dca04daed705fd831"

# Заглавие
st.title("🌍 Персонализирано Време и Качество на Въздуха")

# Въвеждане на град
city = st.text_input("Въведи име на град:", "Plovdiv")

if city:
    # Заявка за времето
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    weather_response = requests.get(weather_url)

    if weather_response.status_code == 200:
        weather_data = weather_response.json()
        lat = weather_data["coord"]["lat"]
        lon = weather_data["coord"]["lon"]

        # Показване на общи метео данни
        st.subheader(f"📍 Времето в {city}")
        st.write(f"🌡 Температура: {weather_data['main']['temp']} °C")
        st.write(f"☁️ Състояние: {weather_data['weather'][0]['description'].title()}")
        st.write(f"💧 Влажност: {weather_data['main']['humidity']}%")
        st.write(f"💨 Вятър: {weather_data['wind']['speed']} m/s")

        # Заявка за данни за замърсяване на въздуха
        pollution_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
        pollution_response = requests.get(pollution_url)

        if pollution_response.status_code == 200:
            pollution_data = pollution_response.json()
            components = pollution_data["list"][0]["components"]
            aqi = pollution_data["list"][0]["main"]["aqi"]

            aqi_meaning = {
                1: "Много добро 🌿",
                2: "Добро 🙂",
                3: "Средно 😐",
                4: "Лошо 😷",
                5: "Много лошо 🚫"
            }

            st.subheader("🫁 Качество на въздуха")
            st.write(f"📊 AQI: {aqi} — {aqi_meaning.get(aqi, 'Няма данни')}")

            df_pollution = pd.DataFrame(components.items(), columns=["Замърсител", "μg/m³"])
            st.dataframe(df_pollution)

            st.subheader("Графика на замърсителите")
            fig, ax = plt.subplots()
            ax.bar(df_pollution["Замърсител"], df_pollution["μg/m³"], color='salmon')
            plt.xticks(rotation=45)
            st.pyplot(fig)

            # Препоръки за безопасни часове
            current_hour = datetime.now().hour
            if 9 <= current_hour <= 13:
                st.success("🌞 Най-доброто време за излизане навън е между 9:00 и 13:00 часа, когато замърсителите са по-малко.")
            elif 18 <= current_hour <= 20:
                st.success("🌅 Втората най-добра възможност е между 18:00 и 20:00 часа.")
            else:
                st.warning("⚠️ Избягвайте излизане между 7:00 и 9:00 часа и между 17:00 и 19:00 часа, когато замърсителите са най-високи.")

            # Съвети за физическа активност
            st.markdown("### 🏃‍♂️ Съвети за безопасна физическа активност:")
            st.write("- Избягвайте интензивни упражнения на открито, когато AQI е над 100.")
            st.write("- Използвайте маска N95 или KN95, за да намалите вдишването на фини частици.")
            st.write("- Предпочитайте дейности на закрито при високи нива на замърсяване.")
            st.write("- Пийте много вода и се хранете с храни, богати на антиоксиданти, за да намалите възпаленията.")
        else:
            st.warning("Неуспешно зареждане на данни за въздуха.")
    else:
        st.error("Градът не бе намерен.")
