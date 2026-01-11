import requests
import time
from core.config import settings

def get_weather_forecast(location: str) -> str:
    """Returns a simplified, well-formatted weather forecast for WhatsApp."""
    api_key = settings.WEATHER_API_KEY
    if not api_key:
        return "Error: Weather API key not configured."
    
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": location, "appid": api_key, "units": "metric"}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        weather_desc = data['weather'][0]['description']
        
        advisory = "Weather seems favorable for normal farming activities."
        if "rain" in weather_desc.lower():
            advisory = "Rain expected. Ensure proper drainage and protect crops if necessary."
        elif temp > 35:
            advisory = "High temperatures expected. Ensure adequate irrigation for crops."

        report = (f"🌤️ *Weather in {location.capitalize()}*\n\n"
                  f"*- Condition:* {weather_desc.capitalize()}\n"
                  f"*- Temp:* *{temp}°C* (Feels like: {feels_like}°C)\n"
                  f"*- Humidity:* *{humidity}%*\n\n"
                  f"💡 *Advisory:* {advisory}")
        return report

    except requests.exceptions.HTTPError as e:
        return f"Could not retrieve weather for '{location}'. Please check the city name."
    except Exception as e:
        print(f"Weather Error: {e}")
        return "Sorry, I couldn't fetch the weather right now."
