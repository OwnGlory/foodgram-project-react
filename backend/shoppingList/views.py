from collections import defaultdict

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response

from recipe.models import IngredientsRecipe, Recipe
from shoppingList.models import ShoppingList
from shoppingList.serializers import ShoppingListSerializer


class ShoppingListViewSet(viewsets.ModelViewSet):

    http_method_names = ('get', 'post', 'delete')
    serializer_class = ShoppingListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return user.shoppinglist.ingredients.all()

    def create(self, request, recipe_id):
        user = request.user
        if Recipe.objects.filter(id=recipe_id).exists():
            recipe = Recipe.objects.get(id=recipe_id)
        else:
            return Response('Такого рецепта не существует.',
                            status=status.HTTP_400_BAD_REQUEST)
        if ShoppingList.objects.filter(user=user, recipe=recipe).exists():
            return Response(
                {'errors': 'Рецепт уже есть в списке покупок.'},
                status=status.HTTP_400_BAD_REQUEST)
        shopping_list, created = ShoppingList.objects.get_or_create(
            recipe=recipe, user=user
        )
        serializer = ShoppingListSerializer(
            shopping_list, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        shopping_list_item = ShoppingList.objects.filter(user=user,
                                                         recipe=recipe)

        if not shopping_list_item.exists():
            return Response('Рецепт не найден в списке покупок.',
                            status=status.HTTP_400_BAD_REQUEST)

        shopping_list_item.delete()
        return Response('Рецепт удален из списка покупок.',
                        status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        user = request.user
        shopping_list = ShoppingList.objects.filter(user=user)
        ingredients = defaultdict(int)

        for item in shopping_list:
            for ingredient in IngredientsRecipe.objects.filter(
                recipe=item.recipe
            ):
                print(ingredient)
                ingredients[
                    (ingredient.ingredients.name,
                     ingredient.ingredients.measurement_unit)
                ] += ingredient.amount
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename="shopping_list.txt"'
        )

        for ingredient, quantity in ingredients.items():
            response.write(f'{ingredient}: {quantity}\n')

        return response
