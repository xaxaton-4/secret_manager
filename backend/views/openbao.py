from core import app
from openbao.openbao_client import get_client


@app.post('/init')
async def init():
    return await get_client().init_vault()

@app.put('/unseal')
async def unseal():
    return await get_client().unseal_vault()

@app.get('/health')
async def health():
    return await get_client().check_health()
