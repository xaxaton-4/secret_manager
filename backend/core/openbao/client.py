import requests

from django.conf import settings


class OpenbaoClientError(Exception):
    pass


class OpenbaoClient:
    def __init__(self):
        self.base_url = settings.OPENBAO_URL
        self.token = 'korazon123'

    # ----------------- СИСТЕМНЫЕ МЕТОДЫ -----------------
    def check_health(self):
        """Проверка здоровья OpenBao"""
        url = self.get_url('v1/sys/health')
        try:
            response = requests.get(url)
            return response.json()
        except Exception as e:
            raise OpenbaoClientError(f"Health check failed: {str(e)}")

    def get_leader(self):
        """Получение информации о лидере (для HA)"""
        url = self.get_url('v1/sys/leader')
        try:
            response = requests.get(url)
            return response.json()
        except Exception as e:
            raise OpenbaoClientError(f"Get leader failed: {str(e)}")

    def seal_vault(self):
        """Герметизация (seal) OpenBao"""
        if not self.token:
            raise OpenbaoClientError("Token required for seal operation")
        url = self.get_url('v1/sys/seal')
        headers = {"X-Vault-Token": self.token}
        try:
            response = requests.put(url, headers=headers)
            return response.json()
        except Exception as e:
            raise OpenbaoClientError(f"Seal failed: {str(e)}")

    def unseal_vault(self, unseal_key: str):
        """Распечатывание (unseal) OpenBao"""
        url = self.get_url('v1/sys/unseal')
        payload = {'key': unseal_key}
        try:
            response = requests.put(url, json=payload)
            return response.json()
        except Exception as e:
            raise OpenbaoClientError(f"Unseal failed: {str(e)}")

    # ----------------- РАБОТА С СЕКРЕТАМИ KV v2 -----------------
    def read_secret(self, path: str, mount_point: str = "secret"):
        """Чтение секрета"""
        if not self.token:
            raise OpenbaoClientError("Token required for read operation")
        url = self.get_url(f'v1/{mount_point}/data/{path}')
        headers = {"X-Vault-Token": self.token}
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise OpenbaoClientError(f"Read secret failed: {str(e)}")

    def write_secret(self, path: str, data: dict, mount_point: str = "secret"):
        """Запись секрета в OpenBao (KV v2)"""
        if not self.token:
            raise OpenbaoClientError("Token required for write operation")

        url = self.get_url(f'v1/{mount_point}/data/{path}')
        headers = {
            "X-Vault-Token": self.token
        }
        payload = {"data": data}

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise OpenbaoClientError(f"Write secret failed: {str(e)}")

    def update_secret(self, path: str, data: dict, mount_point: str = "secret"):
        """Обновление секрета (синоним write)"""
        return self.write_secret(path, data, mount_point)

    def delete_secret(self, path: str, mount_point: str = "secret"):
        """Удаление секрета"""
        if not self.token:
            raise OpenbaoClientError("Token required for delete operation")
        url = self.get_url(f'v1/{mount_point}/data/{path}')
        headers = {"X-Vault-Token": self.token}
        try:
            response = requests.delete(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise OpenbaoClientError(f"Delete secret failed: {str(e)}")

    def list_secrets(self, path: str = "", mount_point: str = "secret"):
        """Список секретов по пути"""
        if not self.token:
            raise OpenbaoClientError("Token required for list operation")
        url = self.get_url(f'v1/{mount_point}/metadata/{path}')
        headers = {"X-Vault-Token": self.token}
        params = {"list": "true"}
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 404:
                return {"keys": []}
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return {"keys": []}
            raise OpenbaoClientError(f"List secrets failed: {str(e)}")

    def share_to_user(self, user_id: int, resource: str, mount_point: str = 'secret'):
        secret = self.read_secret(f'private/{resource}')
        if not secret:
            raise OpenbaoClientError
        value = secret['data'].get('data', {'v': None})
        self.write_secret(f'{user_id}/{resource}', data=value, mount_point=mount_point)

    def read_secret_metadata(self, path: str, mount_point: str = "secret"):
        """Чтение метаданных секрета"""
        if not self.token:
            raise OpenbaoClientError("Token required for metadata operation")
        url = self.get_url(f'v1/{mount_point}/metadata/{path}')
        headers = {"X-Vault-Token": self.token}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise OpenbaoClientError(f"Read metadata failed: {str(e)}")

    def read_secret_version(self, path: str, version: int, mount_point: str = "secret"):
        """Чтение конкретной версии секрета"""
        if not self.token:
            raise OpenbaoClientError("Token required for version read")
        url = self.get_url(f'v1/{mount_point}/data/{path}')
        headers = {"X-Vault-Token": self.token}
        params = {"version": version}
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise OpenbaoClientError(f"Read secret version failed: {str(e)}")

    # ----------------- УПРАВЛЕНИЕ ПОЛИТИКАМИ -----------------
    def create_policy(self, name: str, policy_rules: dict):
        """Создание политики"""
        if not self.token:
            raise OpenbaoClientError("Token required for policy creation")
        url = self.get_url(f'v1/sys/policies/acl/{name}')
        headers = {"X-Vault-Token": self.token}
        payload = {"policy": policy_rules}
        try:
            response = requests.put(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise OpenbaoClientError(f"Create policy failed: {str(e)}")

    def read_policy(self, name: str):
        """Чтение политики"""
        if not self.token:
            raise OpenbaoClientError("Token required for policy read")
        url = self.get_url(f'v1/sys/policies/acl/{name}')
        headers = {"X-Vault-Token": self.token}
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise OpenbaoClientError(f"Read policy failed: {str(e)}")

    def list_policies(self):
        """Список всех политик"""
        if not self.token:
            raise OpenbaoClientError("Token required for policies list")
        url = self.get_url('v1/sys/policies/acl')
        headers = {"X-Vault-Token": self.token}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise OpenbaoClientError(f"List policies failed: {str(e)}")

    def delete_policy(self, name: str):
        """Удаление политики"""
        if not self.token:
            raise OpenbaoClientError("Token required for policy deletion")
        url = self.get_url(f'v1/sys/policies/acl/{name}')
        headers = {"X-Vault-Token": self.token}
        try:
            response = requests.delete(url, headers=headers)
            response.raise_for_status()
            return response.status_code == 204
        except Exception as e:
            raise OpenbaoClientError(f"Delete policy failed: {str(e)}")

    # ----------------- УПРАВЛЕНИЕ ТОКЕНАМИ -----------------
    def create_token(self, policies: list, ttl: str = "24h", renewable: bool = True):
        """Создание токена"""
        if not self.token:
            raise OpenbaoClientError("Token required for token creation")
        url = self.get_url('v1/auth/token/create')
        headers = {"X-Vault-Token": self.token}
        payload = {
            "policies": policies,
            "ttl": ttl,
            "renewable": renewable
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise OpenbaoClientError(f"Create token failed: {str(e)}")

    def renew_token(self, token: str = None):
        """Продление токена"""
        token_to_renew = token or self.token
        if not token_to_renew:
            raise OpenbaoClientError("Token required for renewal")

        url = self.get_url('v1/auth/token/renew')
        headers = {"X-Vault-Token": self.token} if self.token else {}
        payload = {"token": token_to_renew}
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise OpenbaoClientError(f"Renew token failed: {str(e)}")

    def revoke_token(self, token: str):
        """Отзыв токена"""
        if not self.token:
            raise OpenbaoClientError("Token required for token revocation")
        url = self.get_url('v1/auth/token/revoke')
        headers = {"X-Vault-Token": self.token}
        payload = {"token": token}
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.status_code == 204
        except Exception as e:
            raise OpenbaoClientError(f"Revoke token failed: {str(e)}")

    def lookup_token(self, token: str = None):
        """Информация о токене"""
        token_to_lookup = token or self.token
        if not token_to_lookup:
            raise OpenbaoClientError("Token required for lookup")

        url = self.get_url('v1/auth/token/lookup')
        headers = {"X-Vault-Token": token_to_lookup}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise OpenbaoClientError(f"Token lookup failed: {str(e)}")

    # ----------------- АУТЕНТИФИКАЦИЯ -----------------
    def auth_token(self, token: str):
        """Аутентификация по токену"""
        self.token = token
        return {"status": "authenticated", "token": self.token}

    def auth_userpass(self, username: str, password: str):
        """Аутентификация по логину/паролю"""
        url = self.get_url(f'v1/auth/userpass/login/{username}')
        payload = {"password": password}
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            self.token = data.get("auth", {}).get("client_token")
            if not self.token:
                raise OpenbaoClientError("Userpass auth failed - no token received")
            return data
        except Exception as e:
            raise OpenbaoClientError(f"Userpass auth failed: {str(e)}")

    # ----------------- УТИЛИТЫ -----------------
    def is_authenticated(self):
        """Проверка аутентификации клиента"""
        if not self.token:
            return False
        try:
            result = self.lookup_token()
            return result.get("data", {}).get("expire_time") is not None
        except OpenbaoClientError:
            return False

    def get_url(self, endpoint: str):
        """Формирование полного URL"""
        return f'{self.base_url.rstrip("/")}/{endpoint.lstrip("/")}'

    def set_token(self, token: str):
        """Установка токена"""
        self.token = token

    def get_token(self):
        """Получение текущего токена"""
        return self.token


def get_client():
    if not hasattr(get_client, 'openbao'):
        get_client.openbao = OpenbaoClient()
    return get_client.openbao
