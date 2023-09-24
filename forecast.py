# #!/usr/bin/env python3

import requests

lat, long = 37.8393, -84.2700

response = requests.get("https://api.weather.gov/points/37.8393,-84.2700")
if response.status_code == 200:
    data = response.json()
else:
    print(f"Request for API failed with status code {response.status_code}")
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

print("Latitude: %s | Longitude: %s" % (lat, long))
print("Temperature: %s | Wind Speed: %s | Wind Direction: %s" % (temp, wind_speed, wind_dir))