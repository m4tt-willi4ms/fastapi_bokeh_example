from random import random
from fastapi import FastAPI, Query
import uvicorn

app = FastAPI(title="Random API")


@app.get("/random", tags=["Random Spot Generator"])
async def get_random_numbers(N: int = Query(default=10, gt=0, le=100)):
    return {"spots": [[random(), random()] for i in range(N)]}

def run_server():
    uvicorn.run(app)