from rest_framework import mixins
from rest_framework import filters, viewsets

from .permissions import IsAdminOrReadOnly


class CreateListDestroyViewSet(
        mixins.CreateModelMixin, mixins.ListModelMixin,
        mixins.DestroyModelMixin, viewsets.GenericViewSet):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
