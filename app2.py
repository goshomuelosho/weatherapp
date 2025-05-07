import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# OpenWeatherMap API Key
api_key = "c230b5153f2f086dca04daed705fd831"

# Заглавие
st.title("🌍 Персонализирано Време: Време и Качество на Въздуха")

# Избор на потребителски профил
profile = st.selectbox("Избери профил:", ["Общ потребител", "🫁 Чувствителен към въздуха"])

# Въвеждане на град
city = st.text_input("Въведи име на град:", "London")

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

        # === Само ако потребителят е чувствителен към въздуха ===
        if profile == "🫁 Чувствителен към въздуха":
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

                # Препоръки
                st.markdown("📌 **Здравни съвети:**")
                if aqi >= 4:
                    st.error("Препоръчва се да останеш вкъщи.")
                elif aqi == 3:
                    st.warning("Може да предизвика дразнене при чувствителни хора.")
                else:
                    st.success("Няма риск за здравето при нормална активност.")
            else:
                st.warning("Неуспешно зареждане на данни за въздуха.")

    else:
        st.error("Градът не бе намерен.")
