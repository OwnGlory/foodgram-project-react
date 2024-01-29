import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from favourite.models import Favourite
from ingredients.models import Ingredients
from ingredients.serializers import (
    IngredientsAddRecipeSerializer,
    IngredientsRecipeSerializer)
from recipe.models import Tag, Recipe, TagRecipe, IngredientsRecipe
from users.serializers import UserSerializer


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipeListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    image = Base64ImageField(required=True)
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'image',
                  'name', 'text', 'is_favorited', 'cooking_time')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['ingredients'] = IngredientsRecipeSerializer(
            instance.ingredients.all(),
            many=True,
            context={'recipe_id': instance.id}
        ).data
        return representation

    def get_is_favorited(self, instance):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Favourite.objects.filter(
                user=request.user, recipe=instance
            ).exists()
        return False


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = IngredientsAddRecipeSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    image = Base64ImageField()
    author = UserSerializer(
        read_only=True
    )

    class Meta:
        model = Recipe
        fields = ('id', 'ingredients', 'tags', 'image', 'name', 'text',
                  'cooking_time', 'author')

    def create_ingredients(self, ingredients, recipe):
        IngredientsRecipe.objects.bulk_create(
            [IngredientsRecipe(
                ingredients=Ingredients.objects.get(id=ingredient.get('id')),
                recipe=recipe,
                amount=ingredient.get('amount')
            ) for ingredient in ingredients]
        )

    def create_tags(self, tags, recipe):
        TagRecipe.objects.bulk_create(
            [TagRecipe(recipe=recipe, tag=tag) for tag in tags]
        )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        user = self.context['request'].user
        validated_data['author'] = user
        recipe = Recipe.objects.create(**validated_data)
        recipe.save()
        self.create_ingredients(ingredients, recipe)
        self.create_tags(tags, recipe)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        TagRecipe.objects.filter(recipe=instance).delete()
        IngredientsRecipe.objects.filter(recipe=instance).delete()
        self.create_ingredients(ingredients, instance)
        self.create_tags(tags, instance)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeListSerializer(instance, context={
            '  request': self.context.get('request')}).data
