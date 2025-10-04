from aiohttp import ClientSession
from config import settings


class OpenbaoClientError(Exception):
    pass


class OpenbaoClient:
    base_url = settings.OPENBAO_BASE_URL

    unseal_key = None

    async def get_url(self, endpoint: str):
        return f'{self.base_url.rstrip("/")}/{endpoint.lstrip("/")}'


# ----------------- АУТЕНТИФИКАЦИЯ -----------------
    async def auth_token(self, token: str):
        """Аутентификация по токену"""
        self.token = token
        return {"status": "authenticated", "token": self.token}

    async def auth_userpass(self, username: str, password: str):
        """Аутентификация по логину/паролю"""
        url = await self.get_url("v1/auth/userpass/login/" + username)
        async with ClientSession() as session:
            async with session.post(url, json={"password": password}) as response:
                data = await response.json()
                self.token = data.get("auth", {}).get("client_token")
                if not self.token:
                    raise OpenbaoClientError("Userpass auth failed")
                return data

    async def auth_approle(self, role_id: str, secret_id: str):
        """Аутентификация через AppRole"""
        url = await self.get_url("v1/auth/approle/login")
        async with ClientSession() as session:
            async with session.post(url, json={"role_id": role_id, "secret_id": secret_id}) as response:
                data = await response.json()
                self.token = data.get("auth", {}).get("client_token")
                if not self.token:
                    raise OpenbaoClientError("AppRole auth failed")
                return data

    # ----------------- РАБОТА С СЕКРЕТАМИ -----------------
    async def read_secret(self, path: str):
        url = await self.get_url(f"v1/secret/data/{path}")
        headers = {"X-Vault-Token": self.token}
        async with ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                return await response.json()

    async def write_secret(self, path: str, data: dict):
        url = await self.get_url(f"v1/secret/data/{path}")
        headers = {"X-Vault-Token": self.token}
        payload = {"data": data}
        async with ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                return await response.json()

    async def list_secrets(self, path: str):
        url = await self.get_url(f"v1/secret/metadata/{path}?list=true")
        headers = {"X-Vault-Token": self.token}
        async with ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                return await response.json()

    async def delete_secret(self, path: str):
        url = await self.get_url(f"v1/secret/data/{path}")
        headers = {"X-Vault-Token": self.token}
        async with ClientSession() as session:
            async with session.delete(url, headers=headers) as response:
                return await response.json()

    # ----------------- УПРАВЛЕНИЕ ПОЛИТИКАМИ -----------------
    async def create_policy(self, name: str, rules: str):
        url = await self.get_url(f"v1/sys/policies/acl/{name}")
        headers = {"X-Vault-Token": self.token}
        payload = {"policy": rules}
        async with ClientSession() as session:
            async with session.put(url, headers=headers, json=payload) as response:
                return await response.json()

    async def read_policy(self, name: str):
        url = await self.get_url(f"v1/sys/policies/acl/{name}")
        headers = {"X-Vault-Token": self.token}
        async with ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                return await response.json()

    async def delete_policy(self, name: str):
        url = await self.get_url(f"v1/sys/policies/acl/{name}")
        headers = {"X-Vault-Token": self.token}
        async with ClientSession() as session:
            async with session.delete(url, headers=headers) as response:
                return await response.json()

    # ----------------- РАБОТА С ТОКЕНАМИ -----------------
    async def create_token(self, policies: list, ttl: str = "24h"):
        url = await self.get_url("v1/auth/token/create")
        headers = {"X-Vault-Token": self.token}
        payload = {"policies": policies, "ttl": ttl}
        async with ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                return await response.json()

    async def renew_token(self, token: str):
        url = await self.get_url("v1/auth/token/renew")
        headers = {"X-Vault-Token": self.token}
        payload = {"token": token}
        async with ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                return await response.json()

    async def revoke_token(self, token: str):
        url = await self.get_url("v1/auth/token/revoke")
        headers = {"X-Vault-Token": self.token}
        payload = {"token": token}
        async with ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                return await response.json()

    # ----------------- СИСТЕМНЫЕ ОПЕРАЦИИ -----------------

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

    async def seal_vault(self):
        """Герметизация (seal) OpenBao"""
        url = await self.get_url('v1/sys/seal')
        headers = {"X-Vault-Token": self.token} if hasattr(self, "token") else {}
        async with ClientSession() as session:
            try:
                async with session.put(url, headers=headers) as response:
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
