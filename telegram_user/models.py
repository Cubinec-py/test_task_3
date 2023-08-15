from django.db import models


class TelegramUser(models.Model):
    telegram_id = models.BigIntegerField(unique=True, verbose_name="Telegram ID")

    username = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        unique=True,
        verbose_name="Telegram username",
    )

    first_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Telegram first name",
    )

    last_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Telegram last name",
    )

    def __str__(self):
        return self.username if self.username else self.first_name

    class Meta:
        verbose_name = "Telegram User"
        verbose_name_plural = "001. Telegram Users"
