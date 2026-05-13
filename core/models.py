from django.db import models
from django.conf import settings

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(verbose_name="Почта", max_length=255, unique=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name="Пользователь",
        related_name="profile",
        on_delete=models.CASCADE, )

    nickname = models.CharField(verbose_name="Никнейм", max_length=64)

    avatar = models.ImageField(
        verbose_name="Фотография профиля",
        upload_to="avatars/",
        default="avatars/user_placeholder.webp",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return self.nickname