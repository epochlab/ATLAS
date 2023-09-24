# #!/usr/bin/env python3

import libtools

lat, long = 37.8393, -84.2700

data = libtools.echo(f"https://api.weather.gov/points/{lat},{long}")
forecast = libtools.echo(data["properties"]["forecast"])

temp = forecast["properties"]["periods"][0]["temperature"]
wind_speed = forecast["properties"]["periods"][0]["windSpeed"]
wind_dir = forecast["properties"]["periods"][0]["windDirection"]

print("Latitude: %s | Longitude: %s" % (lat, long))
print("Temperature: %s | Wind Speed: %s | Wind Direction: %s" % (temp, wind_speed, wind_dir))