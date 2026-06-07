import requests
from city_coordinates import city_coordinates

def outside_weather(city):
    latitude,longitude = city_coordinates(city)
    
    if latitude is None or longitude is None:
        return None
    
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,relative_humidity_2m,surface_pressure"
    

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        return data.get("current")
    except requests.exceptions.RequestException:
        print("Błąd serwera Open-Meteo.")
        return None