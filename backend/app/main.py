from fastapi import FastAPI
import httpx

app = FastAPI()
OPENBAO_URL = os.getenv("OPENBAO_URL", "http://openbao:8200")

unseal_key = None

@app.post("/init")
async def init_vault():
    global unseal_key
    payload = {
        "secret_shares": 1,
        "secret_threshold": 1
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{OPENBAO_URL}/v1/sys/init", json=payload)
    data = response.json()
    unseal_key= data["keys"][0]
    return data

@app.get("/health")
async def check_health():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{OPENBAO_URL}/v1/sys/health")
    return response.json()

@app.put("/unseal")
async def unseal_vault():
    global unseal_key
    if not unseal_key:
        return {"error": "Vault is not initialized"}
    payload = {"key": unseal_key}
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{OPENBAO_URL}/v1/sys/unseal", json=payload)
    return response.json()
