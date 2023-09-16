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
    client_host = request.client.host
    return {"client_host": client_host}




if __name__ == "__main__":
    run("web:app", port=PORT, log_level="info", host=HOST)