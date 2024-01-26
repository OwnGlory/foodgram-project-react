from django.db import models
from users.models import MyUser


class Subscribe(models.Model):
    user = models.ForeignKey(
        MyUser, on_delete=models.CASCADE,
        related_name='user'
    )
    author = models.ForeignKey(
        MyUser, on_delete=models.CASCADE,
        related_name='author'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author',),
                name='unique_user_author'
            ),
        )

    def __str__(self):
        return f'{self.user} {self.author}'
