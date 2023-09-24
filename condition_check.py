# #!/usr/bin/env python3

import argparse, sys, requests

def echo(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Request failed with status code {response.status_code}")
        exit()

parser = argparse.ArgumentParser()
parser.add_argument('-lat', type=float, default=30.4515)
parser.add_argument('-long', type=float, default=-91.1871)
args = parser.parse_args(sys.argv[1:])

data = echo(f"https://api.weather.gov/points/{args.lat},{args.long}")
forecast = echo(data["properties"]["forecast"])

temp = forecast["properties"]["periods"][0]["temperature"]
wind_speed = forecast["properties"]["periods"][0]["windSpeed"]
wind_dir = forecast["properties"]["periods"][0]["windDirection"]

print(f"Latitude: {args.lat} | Longitude: {args.long}")
print(f"Temperature: {temp} | Wind Speed: {wind_speed} | Wind Direction: {wind_dir}")