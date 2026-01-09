from datetime import datetime
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """
    Get selected city real time weather
    Args:
        city: city name，like New York, Tokyo, Boston, Paris, etc.
    """
    weather_database = {
        "New York": {"condition": "晴天", "temp": "15-25°C", "aqi": "优"},
        "Boston": {"condition": "多云", "temp": "18-28°C", "aqi": "良"},
        "Tokyo": {"condition": "小雨", "temp": "22-30°C", "aqi": "优"},
        "Paris": {"condition": "阴天", "temp": "17-26°C", "aqi": "良"},
        "London": {"condition": "晴天", "temp": "20-32°C", "aqi": "良"},
    }
    if city not in weather_database:
        return f"{city} is N/A, please choose another city like Tokyo, Boston, Paris, etc"
    data = weather_database[city]
    return f"""
    
{city} Weather forecast
━━━━━━━━━━━━━━━━
Weather：{data['condition']}
Temperature：{data['temp']}
Air Quality：{data['aqi']}
Updated time：{datetime.now().strftime("%H:%M")}
    """.strip()