from django.db import models

from recipe.models import Recipe
from users.models import MyUser


class Favourite(models.Model):
    user = models.ForeignKey(
        MyUser, on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favourite'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return f'{self.user} {self.recipe}'
