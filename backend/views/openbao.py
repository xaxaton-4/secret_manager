from core import app
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from openbao.openbao_client import get_client

client = get_client()

router = APIRouter(prefix="/openbao")

# ----------------- МОДЕЛИ ДАННЫХ -----------------
class TokenAuth(BaseModel):
    token: str


class UserPassAuth(BaseModel):
    username: str
    password: str


class AppRoleAuth(BaseModel):
    role_id: str
    secret_id: str


class SecretData(BaseModel):
    data: dict


class PolicyData(BaseModel):
    rules: str


class TokenData(BaseModel):
    policies: list
    ttl: str = "24h"


class TokenRevoke(BaseModel):
    token: str

# ----------------- АУТЕНТИФИКАЦИЯ -----------------
@app.post("/auth/token")
async def auth_token(auth: TokenAuth):
    try:
        return await client.auth_token(auth.token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/auth/userpass")
async def auth_userpass(auth: UserPassAuth):
    try:
        return await client.auth_userpass(auth.username, auth.password)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/auth/approle")
async def auth_approle(auth: AppRoleAuth):
    try:
        return await client.auth_approle(auth.role_id, auth.secret_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----------------- СЕКРЕТЫ -----------------
@app.get("/secret/{path:path}")
async def read_secret(path: str):
    try:
        return await client.read_secret(path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/secret/{path:path}")
async def write_secret(path: str, secret: SecretData):
    try:
        return await client.write_secret(path, secret.data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/secret_list/{path:path}")
async def list_secrets(path: str):
    try:
        return await client.list_secrets(path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/secret/{path:path}")
async def delete_secret(path: str):
    try:
        return await client.delete_secret(path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----------------- ПОЛИТИКИ -----------------
@app.post("/policy/{name}")
async def create_policy(name: str, policy: PolicyData):
    try:
        return await client.create_policy(name, policy.rules)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/policy/{name}")
async def read_policy(name: str):
    try:
        return await client.read_policy(name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/policy/{name}")
async def delete_policy(name: str):
    try:
        return await client.delete_policy(name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----------------- ТОКЕНЫ -----------------
@app.post("/token")
async def create_token(token_data: TokenData):
    try:
        return await client.create_token(token_data.policies, token_data.ttl)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/token/renew")
async def renew_token(token: TokenRevoke):
    try:
        return await client.renew_token(token.token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/token/revoke")
async def revoke_token(token: TokenRevoke):
    try:
        return await client.revoke_token(token.token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----------------- СИСТЕМНЫЕ ОПЕРАЦИИ -----------------
@app.get("/health")
async def health():
    try:
        return await client.check_health()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/unseal")
async def unseal_vault():
    try:
        return await client.unseal_vault()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/seal")
async def seal_vault():
    try:
        return await client.seal_vault()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
