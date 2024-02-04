import logging

from django_filters import rest_framework as filters
from rest_framework import permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination

from recipe.models import Recipe, Tag
from recipe.serializers import (
    TagSerializer,
    RecipeListSerializer,
    RecipeCreateSerializer,
)
from users.permissions import IsAdminOwnerOrReadOnly

logger = logging.getLogger(__name__)


class RecipeFilter(filters.FilterSet):
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )
    author = filters.CharFilter(field_name='author__id')
    tags = filters.CharFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'author', 'is_in_shopping_cart', 'tags')

    def filter_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favourite__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
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
    pagination_class = None
