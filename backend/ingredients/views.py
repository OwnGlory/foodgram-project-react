from django_filters import rest_framework as filters
from rest_framework import permissions, viewsets

from ingredients.models import Ingredients
from ingredients.serializers import IngredientsSerializer


class IngredientsFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Ingredients
        fields = ['name']


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = IngredientsFilter
    serializer_class = IngredientsSerializer
    permission_classes = (permissions.AllowAny,)
