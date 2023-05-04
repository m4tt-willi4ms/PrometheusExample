import random

import prometheus_client
import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from prometheus_client import Counter, Enum, make_asgi_app

prometheus_client.REGISTRY.unregister(prometheus_client.GC_COLLECTOR)
prometheus_client.REGISTRY.unregister(prometheus_client.PLATFORM_COLLECTOR)
prometheus_client.REGISTRY.unregister(prometheus_client.PROCESS_COLLECTOR)


c = Counter("test_counter", "A test counter")
e = Enum("test_state", "A test state", states=["starting", "running", "stopped"])
e.state("running")

app = FastAPI()

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url="/docs")


@app.get("/test")
def test():
    c.inc()
    # Update state randomly
    new_state = random.choice(["starting", "running", "stopped"])
    e.state(new_state)
    return [c._value.get(), new_state]


uvicorn.run(app, host="0.0.0.0")
