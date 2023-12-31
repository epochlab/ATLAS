# #!/usr/bin/env python3

import argparse, sys, requests

def echo(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['properties']
    else:
        print(f"Request failed with status code {response.status_code}")
        exit()

parser = argparse.ArgumentParser()
parser.add_argument('-lat', type=float, default=30.4515)
parser.add_argument('-long', type=float, default=-91.1871)
args = parser.parse_args(sys.argv[1:])

data = echo(f"https://api.weather.gov/points/{args.lat},{args.long}")
forecast = echo(data["forecast"])

city = data['relativeLocation']['properties']['city']
state = data['relativeLocation']['properties']['state']
print(f"Lat|Long: [{args.lat}, {args.long}]")
print(f"City: {city} | State: {state}")

temp = forecast["periods"][0]["temperature"]
wind_speed = forecast["periods"][0]["windSpeed"]
wind_dir = forecast["periods"][0]["windDirection"]
start_time = forecast["periods"][0]["startTime"]

print(start_time)
print(f"Temperature: {temp} | Wind Speed: {wind_speed} | Wind Direction: {wind_dir}")