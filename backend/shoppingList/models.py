from django.db import models

from recipe.models import Recipe
from users.models import MyUser


class ShoppingList(models.Model):

    user = models.ForeignKey(
        MyUser, on_delete=models.CASCADE,
        verbose_name='Авторизированный пользователь'
    )

    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='shoppinglist'
    )

    class Meta:
        verbose_name = 'Список покупок'

    def __str__(self):
        return f'{self.user} {self.recipe}'
