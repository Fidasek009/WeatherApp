import json

with open('weather_conditions.json', 'r') as f:
    data = json.load(f)

output: dict[int, dict[str, str]] = {}

for condition in data:
    output[condition['code']] = {
        "day": condition['day'],
        "dayVideo": condition['icon'],
        "night": condition['night'],
        "nightVideo": condition['icon']
    }

with open('weather.json', 'w') as f:
    json.dump(output, f, indent=4, sort_keys=True)