from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractUser):

    username_validator = UnicodeUsernameValidator

    class Roles(models.TextChoices):
        USER = 'user', 'User'
        ADMIN = 'admin', 'Admin'

    username = models.CharField(
        verbose_name='Уникальный юзернейм',
        max_length=150,
        unique=True,
        help_text='Только буквы, цифры и @/./+/-/_.',
        validators=(username_validator,))

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=254,
        unique=True)

    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True)

    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=True)

    role = models.CharField(
        verbose_name='Права доступа',
        default=Roles.USER,
        choices=Roles.choices,
        max_length=25)

    password = models.CharField(
        verbose_name="Пароль",
        max_length=150)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username

    @property
    def is_admin(self):
        return self.role == self.Roles.ADMIN

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name', 'password')


class Subscription(models.Model):

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='subscriptions',
                             verbose_name='Подписчик')

    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='subscribers',
                               verbose_name='Автор на которого подписан')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'], name='unique')]

    def __str__(self) -> str:
        return f'{self.user} подписан на {self.author}'
