from django.db import models
from telegram_user.models import TelegramUser


class CashSaving(models.Model):
    class SavingType(models.TextChoices):
        Bankaccounts = "Bank Accounts"
        Termdeposits = "Term Deposits"
        Securitiesinvestments = "Securities Investments"
        Retirementsavings = "Retirement Savings"
        Otherinvestments = "Other Investments"
        Emergencyfund = "Emergency Fund"
        Educationsavings = "Education Savings"
        Bigpurchasefund = "Big Purchase Fund"
        Vacationfund = "Vacation Fund"
        Targetedsavings = "Targeted Savings"

    user = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        related_name="user_cash_savings",
        verbose_name="Telegram User",
    )

    saving_type = models.CharField(
        max_length=50,
        choices=SavingType.choices,
        verbose_name="Saving Type",
    )

    amount = models.FloatField(verbose_name="savings Amount", default=0)

    def __str__(self):
        return f"{self.saving_type}: {self.amount}$"

    class Meta:
        verbose_name = "Cash Saving"
        verbose_name_plural = "001. Cash Savings"
