from os import path
import requests
import json
from datetime import datetime
from uvicorn import run
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


HOST="127.0.0.1"
PORT = 4080
WEBDIR = "{0}/html".format(path.dirname(__file__))
TEMPLATES = Jinja2Templates(directory=f"{WEBDIR}/templates")
WEATHER = json.load(open('weather.json', 'r'))

app = FastAPI()
app.mount("/static", StaticFiles(directory=f"{WEBDIR}/static"), name="static")
app.mount("/video", StaticFiles(directory=f"{WEBDIR}/video"), name="video")


@app.get("/", response_class=HTMLResponse)
def weather(request: Request, lat: float = None, lon: float = None):
    geolocation = False
    if lon and lat:
        geolocation = True
        weather = requests.get(f"https://api.weatherapi.com/v1/current.json?key=8da8951ed8694b8782c90333231609&aqi=no&q={lat},{lon}")
    else:
        weather = requests.get(f"https://api.weatherapi.com/v1/current.json?key=8da8951ed8694b8782c90333231609&aqi=no&q={request.client.host}")
    
    current = weather.json()['current']
    condition = current['condition']

    day = "day" if current['is_day'] else "night"
    code = condition['code']
    vidNum = WEATHER[str(code)]['video']
    if code == 1000 and current['is_day']:
        
        currentTime = datetime.fromtimestamp(current['last_updated_epoch'])
        hour = currentTime.hour
        
        dayPart = "evening"           # 17-21 evening
        if hour > 6 and hour < 10:
            dayPart = "morning"     # 6-10 morning
        elif hour < 17:
            dayPart = "noon"        # 10-17 noon

        vidPath = f"/video/{day}/{vidNum}-{dayPart}.mp4"
    else:
        vidPath = f"/video/{day}/{vidNum}.mp4"

    vidPath = "/video/day/1-morning.mp4" # ONLY FOR TESTING

    return TEMPLATES.TemplateResponse("site.j2", {"request": request, "condition": condition, "video": vidPath, "geo": geolocation})





if __name__ == "__main__":
    run("web:app", port=PORT, log_level="info", host=HOST)