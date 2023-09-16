from os import path

import requests
from uvicorn import run
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse


HOST="5.182.17.134"
PORT = 4080
WEBDIR = "{0}/html".format(path.dirname(__file__))

app = FastAPI()
app.mount("/static", StaticFiles(directory=f"{WEBDIR}/static"), name="static")
app.mount("/video", StaticFiles(directory=f"{WEBDIR}/video"), name="video")


url = "https://tools.keycdn.com/geo.json?host="
headers = {
    "User-Agent": "keycdn-tools:https://.kenolas.xyz"
}


@app.get("/")
def weather(request: Request):
    client_host = request.client.host

    # response = requests.get(url + client_host, headers=headers)
    # location = response.json()['data']['geo']

    # weather = request.get(f"https://api.weatherapi.com/v1/current.json?key=8da8951ed8694b8782c90333231609&q={location['latitude']},{location['longitude']}")
    weather = requests.get(f"https://api.weatherapi.com/v1/current.json?key=8da8951ed8694b8782c90333231609&aqi=no&q={client_host}")
    condition = weather.json()['current']['condition']

    return HTMLResponse(f"<body><h1><img src=\"https:{condition['icon']}\" />{condition['text']}</h1><p>{weather.json()}</p></body>")

    return weather.json()




if __name__ == "__main__":
    run("web:app", port=PORT, log_level="info", host=HOST)