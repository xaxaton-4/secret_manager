from fastapi import FastAPI
from openbao_client import init_vault, unseal_vault, check_health

app = FastAPI()

@app.post("/init")
async def init():
    return await init_vault()

@app.put("/unseal")
async def unseal():
    return await unseal_vault()

@app.get("/health")
async def health():
    return await check_health()
