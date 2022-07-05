from random import random
from threading import Thread
import asyncio
import logging

from fastapi import FastAPI, Query, Request
from fastapi.templating import Jinja2Templates
from bokeh.server.server import Server
from bokeh.embed import server_document
from tornado.ioloop import IOLoop
import uvicorn

import plot_slider

# Because of https://github.com/tornadoweb/tornado/issues/775
# this code is required to avoid a call to logging.basicConfig() when using tornado
log = logging.getLogger('tornado')
handler = logging.NullHandler()
log.addHandler(handler)

app = FastAPI()
templates = Jinja2Templates(directory='.')

@app.get("/random", tags=["Random Spot Generator"])
async def get_random_numbers(N: int = Query(default=10, gt=0, le=100)):
    return {"spots": [[random(), random()] for i in range(N)]}


@app.get("/random/plot", tags=["Random Spot Generator"])
def get_random_numbers_plot(request: Request):
    script = server_document("http://localhost:8001/plot-slider")
    return templates.TemplateResponse(
        "template.html",
        {"script": script, "request": request, "framework": "FastAPI"},
    )

def start_bokeh_server():
    server = Server(
        {
            "/plot-slider": plot_slider.add_figure,
        },
        io_loop=IOLoop(),
        address="localhost",
        port=8001,
        allow_websocket_origin=["localhost:8000", "localhost:8001"],
    )
    server.start()
    server.io_loop.start()

def run_server():
    bokeh_thread = Thread(target=start_bokeh_server, daemon=True)
    bokeh_thread.start()
    uvicorn.run(app, host="localhost", port=8000)