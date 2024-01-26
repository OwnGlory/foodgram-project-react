from rest_framework import serializers
from ingredients.models import Ingredients
from recipe.models import IngredientsRecipe


class IngredientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredients
        fields = ('id', 'name', 'measurement_unit')


class IngredientsAddRecipeSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientsRecipe
        fields = ('id', 'amount')


class IngredientsRecipeSerializer(serializers.ModelSerializer):

    amount = serializers.SerializerMethodField()

    class Meta:
        model = Ingredients
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def get_amount(self, obj):
        recipe_id = self.context.get('recipe_id')
        ingredient_recipe = IngredientsRecipe.objects.filter(
            ingredients=obj, recipe_id=recipe_id
        ).first()
        if ingredient_recipe:
            return ingredient_recipe.amount
        return None
