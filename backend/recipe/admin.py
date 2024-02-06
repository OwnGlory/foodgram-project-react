from django.contrib import admin

from recipe.models import Recipe, Tag, TagRecipe, IngredientsRecipe
from favourite.models import Favourite


class TagInline(admin.StackedInline):
    model = TagRecipe
    extra = 0


class IngredientsInline(admin.StackedInline):
    model = IngredientsRecipe
    extra = 0


class RecipeAdmin(admin.ModelAdmin):
    inlines = (
        TagInline,
        IngredientsInline
    )
    list_display = ('name', 'favorites_count',)
    list_filter = ('name', 'author', 'tags')

    def favorites_count(self, obj):
        return Favourite.objects.filter(recipe=obj).count()
    favorites_count.short_description = 'Количество добавлений в избранное'

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
admin.site.register(TagRecipe)
admin.site.register(IngredientsRecipe)
