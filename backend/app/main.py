from fastapi import FastAPI
from .openbao_client import OpenBaoClient

app = FastAPI()
client = OpenBaoClient()

@app.get("/openbao/health")
def openbao_health():
    return client.health()
