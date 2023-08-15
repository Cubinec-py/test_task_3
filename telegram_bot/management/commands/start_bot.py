from django.core.management.base import BaseCommand
from telegram_bot.main import CashSavingBot


class Command(BaseCommand):
    help = "Start the bot."

    def handle(self, *args, **options):
        CashSavingBot().bot.infinity_polling()
