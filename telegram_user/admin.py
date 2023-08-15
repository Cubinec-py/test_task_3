from django.contrib import admin
from telegram_user.models import TelegramUser


@admin.register(TelegramUser)
class CashSavingAdmin(admin.ModelAdmin):
    list_display = [
        "telegram_id",
        "username",
        "first_name",
        "last_name",
    ]
    search_fields = ["telegram_id", "username"]
