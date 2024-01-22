from rest_framework import viewsets, mixins, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from favourite.serializers import FavouriteSerializer
from favourite.models import Favourite
from recipe.models import Recipe


class FavouriteViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    http_method_names = ('post', 'delete')
    serializer_class = FavouriteSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return user.recipe.all()

    def create(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if Favourite.objects.filter(user=user, recipe=recipe).exists():
            return Response(
                {'errors': 'Рецепт уже в избранном.'},
                status=status.HTTP_400_BAD_REQUEST)
        queryset = Favourite.objects.create(recipe=recipe, user=user)
        serializer = FavouriteSerializer(
            queryset, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        favorite = Favourite.objects.filter(recipe=recipe, user=user)
        favorite.delete()
        return Response('Рецепт удален из избранного.',
                        status=status.HTTP_204_NO_CONTENT)
