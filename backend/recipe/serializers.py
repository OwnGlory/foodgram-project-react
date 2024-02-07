import base64

from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from favourite.models import Favourite
from ingredients.models import Ingredients
from ingredients.serializers import (
    IngredientsAddRecipeSerializer,
    IngredientsRecipeSerializer)
from recipe.models import Tag, Recipe, TagRecipe, IngredientsRecipe
from shoppingList.models import ShoppingList
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
    image = serializers.SerializerMethodField('get_image_url')
    author = UserSerializer(
        read_only=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'image',
                  'name', 'text', 'is_favorited', 'is_in_shopping_cart',
                  'cooking_time')

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

    def get_is_in_shopping_cart(self, instance):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return ShoppingList.objects.filter(
                user=request.user, recipe=instance
            ).exists()
        return False

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None


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
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        user = self.context['request'].user
        validated_data['author'] = user

        if not ingredients_data:
            raise ValidationError("В запросе должен быть"
                                  "хотя бы один ингредиент")
        if not tags_data:
            raise ValidationError("Теги отсутствуют в запросе")

        if len(ingredients_data) != len(set(
            [ingredient.get('id') for ingredient in ingredients_data]
        )):
            raise ValidationError("Ингредиенты в запросе"
                                  "не должны повторяться")

        if len(tags_data) != len(set(
            [tag.id for tag in tags_data]
        )):
            raise ValidationError("Теги в запросе"
                                  "не должны повторяться")

        for ingredient in ingredients_data:
            if not Ingredients.objects.filter(id=ingredient['id']).exists():
                raise ValidationError("Ингредиент не найден")
            if ingredient.get('amount') < 1:
                raise ValidationError("Количество ингредиента"
                                      "не может быть < 1")

        for tag in tags_data:
            if not Tag.objects.filter(id=tag.id).exists():
                raise ValidationError("Тег не найден")

        recipe = Recipe.objects.create(**validated_data)
        recipe.save()
        self.create_ingredients(ingredients_data, recipe)
        self.create_tags(tags_data, recipe)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients', None)
        tags_data = validated_data.pop('tags', None)
        TagRecipe.objects.filter(recipe=instance).delete()
        IngredientsRecipe.objects.filter(recipe=instance).delete()

        if not ingredients_data:
            raise ValidationError("В запросе должен быть"
                                  "хотя бы один ингредиент")
        if not tags_data:
            raise ValidationError("Теги отсутствуют в запросе")

        if len(ingredients_data) != len(set(
            [ingredient.get('id') for ingredient in ingredients_data]
        )):
            raise ValidationError("Ингредиенты в запросе"
                                  "не должны повторяться")

        if len(tags_data) != len(set(
            [tag.id for tag in tags_data]
        )):
            raise ValidationError("Теги в запросе"
                                  "не должны повторяться")

        for ingredient in ingredients_data:
            if not Ingredients.objects.filter(id=ingredient['id']).exists():
                raise ValidationError("Ингредиент не найден")
            if ingredient.get('amount') < 1:
                raise ValidationError("Количество ингредиента"
                                      "не может быть < 1")

        for tag in tags_data:
            if not Tag.objects.filter(id=tag.id).exists():
                raise ValidationError("Тег не найден")

        self.create_ingredients(ingredients_data, instance)
        self.create_tags(tags_data, instance)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeListSerializer(instance, context={
            'request': self.context.get('request')}).data


class SubscribeRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
