import yaml, requests

def load_config(file):
    with open(file, 'r') as f:
        return yaml.safe_load(f)
    
def sec2time(secs):
    hrs = int(secs // 3600)
    r_secs = secs % 3600
    mins = int(r_secs // 60)
    r_secs = r_secs % 60
    return hrs, mins, r_secs

def echo(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Request failed with status code {response.status_code}")
        exit()