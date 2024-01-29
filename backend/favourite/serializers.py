from rest_framework import serializers

from favourite.models import Favourite


class FavouriteSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(source='recipe.id', read_only=True)
    name = serializers.CharField(source='recipe.name', read_only=True)
    cooking_time = serializers.IntegerField(source='recipe.cooking_time',
                                            read_only=True)
    image = serializers.ImageField(source='recipe.image', read_only=True)

    class Meta:
        model = Favourite
        fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favourite
        fields = ('id', 'name', 'color')
