from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from subscribe.models import Subscribe
from recipe.models import Recipe
from recipe.serializers import RecipeListSerializer


class SubscribeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для работы с данными модели Subscribe.
    """
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscribe
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
        validators = (
            UniqueTogetherValidator(
                queryset=Subscribe.objects.all(),
                fields=('user', 'author',),
                message="Нельзя подписаться второй раз."
            ),
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscribe.objects.filter(user=request.user,
                                            author=obj.author).exists()
        return False

    def get_recipes(self, obj):
        recipes_limit = int(
            self.context['request'].query_params.get('recipes_limit', 3)
        )
        recipes = Recipe.objects.filter(
            author=obj.author
        )[
            :recipes_limit
        ]
        return RecipeListSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()
