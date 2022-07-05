from random import random

from bokeh.plotting import figure, curdoc
from bokeh.layouts import column
import requests

def get_spots(N):
    try:
        response = requests.get("http://localhost:8000/random", params={"N": N}).json()
    except Exception as e:
        # If the server's not running, using stand-in values instead
        response = {"spots": [[random(), random()] for _ in range(N)]}
    spots = response["spots"]
    return {
        "x": [spot[0] for spot in spots],
        "y": [spot[1] for spot in spots],
    }

def add_figure(doc):
    p = figure()

    data = get_spots(10)

    p.circle("x", "y", source=data)

    doc.add_root(column(p))

doc = curdoc()
add_figure(doc)