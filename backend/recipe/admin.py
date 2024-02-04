from django.contrib import admin

from recipe.models import Recipe, Tag, TagRecipe, IngredientsRecipe

admin.site.register(Recipe)
admin.site.register(Tag)
admin.site.register(TagRecipe)
admin.site.register(IngredientsRecipe)
