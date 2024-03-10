from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response


class PutNotAllowed(mixins.UpdateModelMixin):
    def update(self, request, *args, **kwargs):
        if kwargs.get('partial'):
            return super().update(request, *args, **kwargs)
        return Response({'detail': 'Method "PUT" not allowed.'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)
