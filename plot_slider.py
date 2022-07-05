from random import random

from bokeh.plotting import figure, curdoc
from bokeh.layouts import column
from bokeh.models import Slider, ColumnDataSource
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
    N = 10
    source = ColumnDataSource(data=get_spots(N))
    p = figure(x_range=[0,1], y_range=[0,1])
    p.circle("x", "y", source=source)


    def callback(attr, old, new):
        source.data = get_spots(new)

    slider = Slider(start=1, end=100, value=N, title="Number of spots")
    slider.on_change("value", callback)

    doc.add_root(column(p, slider))

doc = curdoc()
add_figure(doc)