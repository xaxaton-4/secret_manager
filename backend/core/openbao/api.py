from rest_framework.response import Response

from secrets_api.base_api import BaseApiView
from openbao.client import get_client
from users.decorators import with_authorization, only_admin


class SecretDetail(BaseApiView):
    @with_authorization
    def get(self, request):
        openbao_client = get_client()

        account_id = request.user.pk
        resource = request.GET.get('resource')
        secret = openbao_client.read_secret(f'{account_id}/{resource}')
        if secret is None:
            return Response(status=404)
        return Response({'value': secret['data'].get('data', {'v': None}).get('v')})


class SecretList(BaseApiView):
    @with_authorization
    def get(self, request):
        openbao_client = get_client()
        account_id = request.user.pk

        secrets = openbao_client.list_secrets(f'{account_id}/')
        if not secrets:
            return Response([])
        return Response(secrets.get('data', {}).get('keys', []))


class SecretCreate(BaseApiView):
    @only_admin
    def post(self, request):
        openbao_client = get_client()
        try:
            resource = request.data.get('resource')
            value = {'v': request.data.get('value')}
            openbao_client.write_secret(f'private/{resource}', value)
            return Response(status=200)
        except Exception:
            return Response(status=400)
