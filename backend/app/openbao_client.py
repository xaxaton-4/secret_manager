import os
import httpx

class OpenBaoClient:
    def __init__(self):
        # Читаем токен из файла
        token_file = os.getenv("BAO_TOKEN_FILE", "/openbao/file/.bao_token")
        with open(token_file, "r") as f:
            self.token = f.read().strip()

        self.base_url = os.getenv("OPENBAO_URL", "http://openbao:8200")

    def health(self):
        url = f"{self.base_url}/v1/sys/health"
        headers = {"X-Bao-Token": self.token}
        resp = httpx.get(url, headers=headers)
        return resp.json()
