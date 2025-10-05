from secrets_api.base_api import BaseApiView
from openbao.client import get_client


class SecretDetail(BaseApiView):
    def get(self, request):
        openbao_client = get_client()
        print(openbao_client.read_secret('/test'))


class SecretCreate(BaseApiView):
    def get(self, request):
        openbao_client = get_client()
        openbao_client.write_secret('/test', {'1': True})
