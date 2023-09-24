# #!/usr/bin/env python3

import requests

lat, long = 37.8393, -84.2700

location_url = "https://api.weather.gov/points/37.8393,-84.2700"

response = requests.get(location_url)

if response.status_code == 200:
    data = response.json()
else:
    print(f"Request failed with status code {response.status_code}")
    exit()

forecast_response = requests.get(data["properties"]["forecast"])

if forecast_response.status_code == 200:
    forecast_data = forecast_response.json()
else:
    print(f"Request for forecast data failed with status code {forecast_response.status_code}")
    exit()

temp = forecast_data["properties"]["periods"][0]["temperature"]
wind_speed = forecast_data["properties"]["periods"][0]["windSpeed"]
wind_dir = forecast_data["properties"]["periods"][0]["windDirection"]

print("Latitude:", lat, "Longitude", long)
print("Temperature:", temp, "| Wind Speed:", wind_speed, "| Wind Direction", wind_dir)