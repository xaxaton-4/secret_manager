import logging

from rest_framework.response import Response

from secrets_api.base_api import BaseApiView
from openbao.client import get_client
from users.decorators import with_authorization, only_admin


logger = logging.getLogger('core')


"""
@api {GET} /api/secrets/detail/?resource= SecretDetail
@apiGroup Secret

@apiParam {String} resource Секрет, информацию о котором необходимо получить.

@apiSuccess (Ответ) {String} value Расшифрованное значение секрета.
"""
class SecretDetail(BaseApiView):
    @with_authorization
    def get(self, request):
        openbao_client = get_client()

        account_id = request.user.pk
        resource = request.GET.get('resource')
        secret = openbao_client.read_secret(f'{account_id}/{resource}')
        if secret is None:
            return Response(status=404)
        logger.info(f'user {request.user.email} received credentials for {resource}')
        return Response({'value': secret['data'].get('data', {'v': None}).get('v')})


"""
@api {GET} /api/secrets/list/ SecretList
@apiGroup Secret

@apiSuccess (Ответ) {Object[]} secrets Строки.
@apiSuccess (Ответ) {Object[]} secrets.str Название ключа в системе.
"""
class SecretList(BaseApiView):
    @with_authorization
    def get(self, request):
        openbao_client = get_client()
        account_id = request.user.pk

        secrets = openbao_client.list_secrets(f'{account_id}/')
        if not secrets:
            return Response([])
        logger.info(f'list of secrets received by {request.user.email}')
        return Response(secrets.get('data', {}).get('keys', []))


"""
@api {POST} /api/secrets/create/ SecretCreate
@apiGroup Secret

@apiBody {String} resource Секрет, информацию о котором необходимо сохранить.
@apiBody {String} value Значение секрета, зашифрованное стандартом AES.
"""
class SecretCreate(BaseApiView):
    @only_admin
    def post(self, request):
        openbao_client = get_client()
        try:
            resource = request.data.get('resource')
            value = {'v': request.data.get('value')}
            openbao_client.write_secret(f'private/{resource}', value)
            logger.info(f'{request.user.email} create new secret {resource}')
            return Response(status=200)
        except Exception:
            return Response(status=400)
