from rest_framework import viewsets, permissions
from rest_framework.pagination import LimitOffsetPagination
from django_filters import rest_framework as filters
import logging

from users.permissions import IsAdminOwnerOrReadOnly
from recipe.models import Recipe, Tag
from recipe.serializers import (
    RecipeCreateSerializer,
    RecipeListSerializer,
    TagSerializer
)


logger = logging.getLogger(__name__)


class RecipeFilter(filters.FilterSet):
    is_favourite = filters.BooleanFilter(method='filter_is_favourite')
    in_shopping_list = filters.BooleanFilter(method='filter_in_shopping_list')
    author = filters.CharFilter(field_name='author__username')
    tags = filters.CharFilter(field_name='tags__name')

    class Meta:
        model = Recipe
        fields = ['is_favourite', 'author', 'in_shopping_list', 'tags']

    def filter_is_favourite(self, queryset, name, value):
        if value:
            return queryset.filter(favorite__user=self.request.user)
        return queryset

    def filter_in_shopping_list(self, queryset, name, value):
        if value:
            return queryset.filter(shoppinglist__user=self.request.user)
        return queryset


class RecipeViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'head', 'patch', 'delete')
    queryset = Recipe.objects.all()
    permission_classes = (IsAdminOwnerOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeListSerializer
        return RecipeCreateSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'id'
