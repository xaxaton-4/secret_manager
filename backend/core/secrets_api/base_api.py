from rest_framework.views import APIView


class BaseApiView(APIView):
    def dispatch(self, request, *args, **kwargs):
        # logging here?
        return super().dispatch(request, *args, **kwargs)
