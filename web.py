from os import path

from uvicorn import run
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles


HOST="127.0.0.1"
PORT = 1443
WEBDIR = "{0}/html".format(path.dirname(__file__))

app = FastAPI()
app.mount("/static", StaticFiles(directory=f"{WEBDIR}/static"), name="static")


@app.get("/")
def weather(request: Request):
    user_ip = request.headers.get('CF-Connecting-IP')
    city = request.headers.get('CF-IPCity')
    country = request.headers.get('CF-IPCountry')
    print(user_ip, '\n', city, '\n', country)
    return {"Error 418: I'm a teapot"}




if __name__ == "__main__":
    run("web:app", port=PORT, log_level="info", host=HOST)