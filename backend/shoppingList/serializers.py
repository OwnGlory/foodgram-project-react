from rest_framework import serializers
from shoppingList.models import ShoppingList


class ShoppingListSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(source='recipe.id', read_only=True)
    name = serializers.CharField(source='recipe.name', read_only=True)
    cooking_time = serializers.IntegerField(source='recipe.cooking_time',
                                            read_only=True)
    image = serializers.ImageField(source='recipe.image', read_only=True)

    class Meta:
        model = ShoppingList
        fields = ('id', 'name', 'image', 'cooking_time')
