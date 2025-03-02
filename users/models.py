from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True,
        verbose_name="Почта",
        help_text="Укажите почту "
    )

    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Укажите номер телефона "
    )

    city = models.CharField(
        max_length=50,
        verbose_name="Город",
        blank=True,
        null=True,
        help_text="Введите город проживания"
    )

    avatar = models.ImageField(
        upload_to='users/avatars',
        blank=True,
        null=True,
        verbose_name='Аватар',
        help_text='Загрузите фотографию'
    )

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"


class Meta:
    verbose_name = 'пользователь'
    verbose_name_plural = "Пользователи"

