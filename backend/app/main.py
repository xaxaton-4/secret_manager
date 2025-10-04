from fastapi import FastAPI, HTTPException
import requests
import os

app = FastAPI()

OPENBAO_URL = os.environ.get("OPENBAO_URL", "http://openbao:8200")
BAO_TOKEN_FILE = os.environ.get("BAO_TOKEN_FILE", "/openbao/file/.bao_token")

def get_root_token():
    """Читает root_token из файла"""
    if not os.path.exists(BAO_TOKEN_FILE):
        raise HTTPException(status_code=500, detail="Root token file not found")
    with open(BAO_TOKEN_FILE, "r") as f:
        data = f.read()
        print(data)
    # Если файл в формате JSON, достаем root_token
    import json
    try:
        print(json.loads(data)["root_token"])
        return json.loads(data)["root_token"]
    except Exception:
        raise HTTPException(status_code=500, detail="Cannot parse root token from file")

@app.get("/check_root_token")
def check_root_token():
    root_token = get_root_token()
    url = f"{OPENBAO_URL}/v1/sys/mounts"
    headers = {"X-Vault-Token": root_token}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return {"status": "ok", "details": resp.json()}
    else:
        raise HTTPException(status_code=403, detail="Invalid root token or permission denied")
