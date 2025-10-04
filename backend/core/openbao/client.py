import requests

from django.conf import settings


class OpenbaoClientError(Exception):
    pass


class OpenbaoClient:
    base_url = settings.OPENBAO_BASE_URL
    unseal_key = None

# ----------------- АУТЕНТИФИКАЦИЯ -----------------
    def auth_token(self, token: str):
        """Аутентификация по токену"""
        self.token = token
        return {"status": "authenticated", "token": self.token}

    def auth_userpass(self, username: str, password: str):
        """Аутентификация по логину/паролю"""
        url = self.get_url("v1/auth/userpass/login/" + username)
        data = requests.post(url, json={"password": password})
        self.token = data.get("auth", {}).get("client_token")
        if not self.token:
            raise OpenbaoClientError("Userpass auth failed")
        return data

    def auth_approle(self, role_id: str, secret_id: str):
        """Аутентификация через AppRole"""
        url = self.get_url("v1/auth/approle/login")
        data = requests.post(url, json={"role_id": role_id, "secret_id": secret_id})
        self.token = data.get("auth", {}).get("client_token")
        if not self.token:
            raise OpenbaoClientError("AppRole auth failed")
        return data

    # ----------------- РАБОТА С СЕКРЕТАМИ -----------------
    def read_secret(self, path: str):
        url = self.get_url(f"v1/secret/data/{path}")
        headers = {"X-Vault-Token": self.token}
        response = requests.get(url, headers=headers)
        return response.json()

    def write_secret(self, path: str, data: dict):
        url = self.get_url(f"v1/secret/data/{path}")
        headers = {"X-Vault-Token": self.token}
        payload = {"data": data}
        response = requests.post(url, headers=headers, json=payload)
        return response.json()

    def list_secrets(self, path: str):
        url = self.get_url(f"v1/secret/metadata/{path}?list=true")
        headers = {"X-Vault-Token": self.token}
        response = requests.get(url, headers=headers)
        return response.json()

    def delete_secret(self, path: str):
        url = self.get_url(f"v1/secret/data/{path}")
        headers = {"X-Vault-Token": self.token}
        response = requests.delete(url, headers=headers)
        return response.json()

    # ----------------- УПРАВЛЕНИЕ ПОЛИТИКАМИ -----------------
    def create_policy(self, name: str, rules: str):
        url = self.get_url(f"v1/sys/policies/acl/{name}")
        headers = {"X-Vault-Token": self.token}
        payload = {"policy": rules}
        response = requests.put(url, headers=headers, json=payload)
        return response.json()

    def read_policy(self, name: str):
        url = self.get_url(f"v1/sys/policies/acl/{name}")
        headers = {"X-Vault-Token": self.token}
        response = requests.get(url, headers=headers)
        return response.json()

    def delete_policy(self, name: str):
        url = self.get_url(f"v1/sys/policies/acl/{name}")
        headers = {"X-Vault-Token": self.token}
        response = requests.delete(url, headers=headers)
        return response.json()

    # ----------------- РАБОТА С ТОКЕНАМИ -----------------
    def create_token(self, policies: list, ttl: str = "24h"):
        url = self.get_url("v1/auth/token/create")
        headers = {"X-Vault-Token": self.token}
        payload = {"policies": policies, "ttl": ttl}
        response = requests.post(url, headers=headers, json=payload)
        return response.json()

    def renew_token(self, token: str):
        url = self.get_url("v1/auth/token/renew")
        headers = {"X-Vault-Token": self.token}
        payload = {"token": token}
        response = requests.post(url, headers=headers, json=payload)
        return response.json()

    def revoke_token(self, token: str):
        url = self.get_url("v1/auth/token/revoke")
        headers = {"X-Vault-Token": self.token}
        payload = {"token": token}
        response = requests.post(url, headers=headers, json=payload)
        return response.json()

    # ----------------- СИСТЕМНЫЕ ОПЕРАЦИИ -----------------

    def unseal_vault(self):
        if not self.unseal_key:
            return {'error': 'Vault is not initialized'}
        payload = {'key': self.unseal_key}
        url = self.get_url('v1/sys/unseal')
        try:
            response = requests.put(url, json=payload)
            data = response.json()
            return data
        except Exception:
            raise OpenbaoClientError

    def seal_vault(self):
        """Герметизация (seal) OpenBao"""
        url = self.get_url('v1/sys/seal')
        headers = {"X-Vault-Token": self.token} if hasattr(self, "token") else {}
        try:
            response = requests.put(url, headers=headers)
            data = response.json()
            return data
        except Exception:
            raise OpenbaoClientError

    def check_health(self):
        url = self.get_url('v1/sys/health')
        try:
            response = requests.get(url)
            data = response.json()
            return data
        except Exception:
            raise OpenbaoClientError

    def get_url(self, endpoint: str):
        return f'{self.base_url.rstrip("/")}/{endpoint.lstrip("/")}'


def get_client():
    if not hasattr(get_client, 'openbao'):
        get_client.openbao = OpenbaoClient()
    return get_client.openbao
