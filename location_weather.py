import streamlit as st
import json
from openai import OpenAI
from geopy.geocoders import Nominatim
import requests

geolocator = Nominatim(user_agent="location_finder")

def get_location_and_weather(latitude, longitude, openai_key, weather_api_key):
    """
    Function to find city, state, and country based on user's geolocation and fetch weather data.
    
    Parameters:
        openai_key (str): OpenAI API key.
        weather_api_key (str): OpenWeatherMap API key.
    
    Returns:
        dict: Weather data and location information.
    """
    geolocator = Nominatim(user_agent="location_finder")
    client = OpenAI(api_key=openai_key)


    location = geolocator.reverse((latitude, longitude), language="en")

    address = location.raw.get('address', {})
    city = address.get('city', '')
    state = address.get('state', '')
    country = address.get('country', '')


    location = f"{city}, {state}, {country}"

    coor_message = f"""
    This is the location {location}, format it in a way so that it is accepted by 
    openweathermap API example if the location is "City of Syracuse,New York, United States"
    format it as "Syracuse, NY", if just "New York,New York,United States" format it as
    "New York City, NY" and only return the formatted location nothing else.
    """

    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": coor_message},
                    {"role": "user", "content": formatted_location}]
    )

    location = stream.choices[0].message.content
    if "," in location:
        formatted_location = location.split(",")[0].strip()

        
    urlbase = "https://api.openweathermap.org/data/2.5/"
    urlweather = f"weather?q={formatted_location}&appid={weather_api_key}"
    url = urlbase + urlweather

    response = requests.get(url)
    data = response.json()

    if data and data.get("main"):
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        temp_min = data['main']['temp_min']
        temp_max = data['main']['temp_max']
        humidity = data['main']['humidity']

    weather_data = {"Temperature":temp,
                    "Feels_like":feels_like,
                    "temp_min":temp_min,
                    "temp_max":temp_max,
                    "humidity":humidity}
    return weather_data, location