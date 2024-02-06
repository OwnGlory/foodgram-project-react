from django.contrib import admin

from ingredients.models import Ingredients


class IngredientAdmin(admin.ModelAdmin):
    list_filter = ('name',)

admin.site.register(Ingredients, IngredientAdmin)
