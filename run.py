from fastapi_bokeh import run_server
import multiprocess as mp
app_process = mp.Process(target=run_server)
app_process.start()