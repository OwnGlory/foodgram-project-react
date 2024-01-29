from django.db import models


class Ingredients(models.Model):

    name = models.CharField(
        max_length=150,
        verbose_name='Название',
        unique=True
    )

    measurement_unit = models.CharField(
        max_length=15,
        verbose_name='Мера измерения',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = (models.UniqueConstraint(
            fields=('name', 'measurement_unit'),
            name='ingredient_name_unit_unique'
        ),)

    def __str__(self):
        return self.name
