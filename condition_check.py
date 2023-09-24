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

city = data['properties']['relativeLocation']['properties']['city']
state = data['properties']['relativeLocation']['properties']['state']

temp = forecast["properties"]["periods"][0]["temperature"]
wind_speed = forecast["properties"]["periods"][0]["windSpeed"]
wind_dir = forecast["properties"]["periods"][0]["windDirection"]

print(f"Lat|Long: [{args.lat}, {args.long}]")
print(f"City: {city} | State: {state}")
print(f"Temperature: {temp} | Wind Speed: {wind_speed} | Wind Direction: {wind_dir}")