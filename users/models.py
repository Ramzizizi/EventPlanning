from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя
    """

    # инициализация полей
    email = models.EmailField(
        verbose_name="E-mail адрес",
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField(verbose_name="Дата рождения")
    is_admin = models.BooleanField(
        default=False, verbose_name="Статус администратора"
    )

    # установка параметров полей
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["username", "date_of_birth"]

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith(
            ("pbkdf2_sha256$", "bcrypt$", "argon2")
        ):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
