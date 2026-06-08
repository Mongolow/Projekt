import requests

def city_coordinates(city_name):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=pl&format=json"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if "results" in data and len(data["results"]) >0:
                latitude = data["results"][0]["latitude"]
                longitude = data["results"][0]["longitude"]
                return latitude, longitude
    except requests.exceptions.RequestException:
        print("Open-Meteo server error.")
        return None, None