from secrets_api.base_api import BaseApiView
from openbao.client import get_client


class SecretDetail(BaseApiView):
    def get(self, request):
        openbao_client = get_client()
        print(openbao_client.read_secret('/test'))


class SecretCreate(BaseApiView):
    def post(self, request):
        openbao_client = get_client()
        try:
            payload = request.data
            result = openbao_client.write_secret('test', payload)
            return self.success(result)
        except Exception as e:
            return self.error(str(e))
