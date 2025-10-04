from aiohttp import ClientSession

from config import settings


class OpenbaoClientError(Exception):
    pass


class OpenbaoClient:
    base_url = settings.OPENBAO_BASE_URL
    unseal_key = None

    async def init_vault(self):
        payload = {'secret_shares': 1, 'secret_threshold': 1}
        url = await self.get_url('v1/sys/init')
        async with ClientSession() as session:
            try:
                async with session.post(url, json=payload) as response:
                    await response.read()
                    data = await response.json()
                    self.unseal_key = data['keys'][0]
                    return data
            except Exception as request_error:
                raise OpenbaoClientError

    async def unseal_vault(self):
        if not self.unseal_key:
            return {'error': 'Vault is not initialized'}
        payload = {'key': self.unseal_key}
        url = await self.get_url('v1/sys/unseal')
        async with ClientSession() as session:
            try:
                async with session.put(url, json=payload) as response:
                    await response.read()
                    data = await response.json()
                    return data
            except Exception as request_error:
                raise OpenbaoClientError

    async def check_health(self):
        url = await self.get_url('v1/sys/health')
        async with ClientSession() as session:
            try:
                async with session.get(url) as response:
                    await response.read()
                    data = await response.json()
                    return data
            except Exception as request_error:
                raise OpenbaoClientError
        return response.json()

    async def get_url(self, endpoint: str):
        return f'{self.base_url.rstrip("/")}/{endpoint.lstrip("/")}'


def get_client():
    if not hasattr(get_client, 'openbao'):
        get_client.openbao = OpenbaoClient()
    return get_client.openbao
