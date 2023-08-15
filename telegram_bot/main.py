import os
import cash_savings

from load_dotenv import load_dotenv

from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


from telegram_user.models import TelegramUser
from cash_savings.models import CashSaving

load_dotenv()


class CashSavingBot:
    def __init__(self):
        self.bot = TeleBot(os.environ.get("API_TOKEN"))
        self.chanel_name = "@TestTaskSavvyServiceBot"
        self.all_cash_savings_types = CashSaving.SavingType.choices
        self.callback_cash_savings_types = {
            cash_saving[1] for cash_saving in self.all_cash_savings_types
        }
        self.callback_cash_savings_methods = {
            "add",
            "remove",
            "delete",
            "back",
            "back_saving",
        }
        self.callback_cash_savings_values = ("5", "10", "100", "1000")

        @self.bot.message_handler(commands=["start"])
        def start_message(message):
            self.welcome_message(message)

        @self.bot.message_handler(commands=["cash_savings"])
        def cash_savings(message):
            self.cash_savings_process(message)

        @self.bot.callback_query_handler(
            lambda query: query.data.split(":")[0] in self.callback_cash_savings_types
        )
        def cash_saving_types(callback_query):
            self.cash_saving_type_process(callback_query.data)

        @self.bot.callback_query_handler(
            lambda query: query.data.split(":")[0] in self.callback_cash_savings_methods
        )
        def cash_saving_methods(callback_query):
            self.cash_saving_methods_process(callback_query)

        @self.bot.callback_query_handler(
            lambda query: query.data.split(":")[0] in self.callback_cash_savings_values
        )
        def callback_cash_savings_values(callback_query):
            self.callback_cash_savings_values_process(callback_query)

        @self.bot.message_handler(func=lambda message: True)
        def echo_message(message):
            self.echo_message_process(message)

    def welcome_message(self, message):
        if not TelegramUser.objects.filter(telegram_id=message.from_user.id).exists():
            TelegramUser.objects.create(
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
            )
        text = (
            f"Hi <b>{message.from_user.first_name}</b>, I am test task bot for Savvy Service company."
            f"\nHere you can add, watch or edit your cash savings!"
            f"\nTo see list of cash savings, use <b>/cash_savings</b> command."
        )
        self.bot.reply_to(message=message, text=text, parse_mode="html")

    def cash_savings_process(
        self, message=None, user_id=None, chat_id=None, edit=False, message_id=None
    ):
        from_user = message.from_user.id if not user_id else user_id
        id_chat = message.chat.id if not chat_id else chat_id
        message_id = int(message.message_id) + 1 if not message_id else message_id
        text = "List of cash savings, to change your amount just click on it:"
        inline_keyboard = InlineKeyboardMarkup()
        user_cash_savings = CashSaving.objects.filter(
            user__telegram_id=from_user
        ).values("saving_type", "amount")
        for saving_type in self.all_cash_savings_types:
            user_amount = 0
            for user_saving_type in user_cash_savings:
                if saving_type[0] in user_saving_type["saving_type"]:
                    user_amount = user_saving_type["amount"]
            user_amount_text = f": {user_amount}$" if user_amount > 0 else ""
            button = InlineKeyboardButton(
                text=f"{saving_type[0]}{user_amount_text}",
                callback_data=f"{saving_type[1]}:{from_user}:{id_chat}:{message_id}",
            )
            inline_keyboard.add(button)
        if not edit:
            self.bot.send_message(
                chat_id=id_chat,
                text=text,
                reply_markup=inline_keyboard,
                parse_mode="html",
            )
            return
        self.bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=inline_keyboard,
            parse_mode="html",
        )

    def cash_saving_type_process(self, callback_query):
        (
            saving_callback_type,
            user_telegram_id,
            chat_id,
            message_id,
        ) = callback_query.split(":")
        saving_type = getattr(CashSaving.SavingType, saving_callback_type)
        try:
            user_amount = CashSaving.objects.get(
                user__telegram_id=user_telegram_id, saving_type=saving_type
            ).amount
        except CashSaving.DoesNotExist:
            user_amount = 0
        inline_keyboard = InlineKeyboardMarkup()
        if user_amount > 0:
            text = (
                f"Here you can add, remove or delete all cash savings for <b>{saving_type}</b>, "
                f"now have <b>{user_amount}$</b>:"
            )
            button_1 = InlineKeyboardButton(
                text="Add cash",
                callback_data=f"add:{saving_callback_type}:{message_id}:{user_telegram_id}:{chat_id}",
            )
            button_2 = InlineKeyboardButton(
                text="Remove cash",
                callback_data=f"remove:{saving_callback_type}:{message_id}:{user_telegram_id}:{chat_id}",
            )
            button_3 = InlineKeyboardButton(
                text=f"Remove all from {saving_type}",
                callback_data=f"delete:{saving_callback_type}:{message_id}:{user_telegram_id}:{chat_id}",
            )
            inline_keyboard.add(button_1)
            inline_keyboard.add(button_2)
            inline_keyboard.add(button_3)
        else:
            text = f"Here you can add and create your cash savings for <b>{saving_type}</b>:"
            button_1 = InlineKeyboardButton(
                text=f"Create {saving_type}",
                callback_data=f"add:{saving_callback_type}:{message_id}:{user_telegram_id}:{chat_id}",
            )
            inline_keyboard.add(button_1)
        button = InlineKeyboardButton(
            text="Back",
            callback_data=f"back:{saving_callback_type}:{message_id}:{user_telegram_id}:{chat_id}",
        )
        inline_keyboard.add(button)
        self.bot.edit_message_text(
            chat_id=chat_id,
            message_id=int(message_id),
            text=text,
            reply_markup=inline_keyboard,
            parse_mode="html",
        )

    def cash_saving_methods_process(self, callback_query):
        (
            method,
            saving_callback_type,
            message_id,
            user_telegram_id,
            chat_id,
        ) = callback_query.data.split(":")
        saving_type = getattr(CashSaving.SavingType, saving_callback_type)
        if method == "delete":
            CashSaving.objects.get(
                user__telegram_id=user_telegram_id, saving_type=saving_type
            ).delete()
            text = f"All cash was deleted from {saving_type}"
            self.bot.answer_callback_query(
                callback_query_id=callback_query.id, text=text, show_alert=False
            )
            self.cash_savings_process(
                user_id=user_telegram_id,
                chat_id=chat_id,
                edit=True,
                message_id=message_id,
            )
            return
        elif method == "back":
            self.cash_savings_process(
                user_id=user_telegram_id,
                chat_id=chat_id,
                edit=True,
                message_id=message_id,
            )
            return
        elif method == "back_saving":
            self.cash_saving_type_process(
                f"{saving_callback_type}:{user_telegram_id}:{chat_id}:{message_id}"
            )
            return
        text = (
            f"Choose value for <b>{saving_type}</b> which you want to <b>{method}</b>"
        )
        inline_keyboard = InlineKeyboardMarkup()
        for amount in self.callback_cash_savings_values:
            button = InlineKeyboardButton(
                text=f"{amount}$",
                callback_data=f"{amount}:{method}:{saving_callback_type}:{message_id}:{user_telegram_id}:{chat_id}",
            )
            inline_keyboard.add(button)
        button = InlineKeyboardButton(
            text="Back",
            callback_data=f"back_saving:{saving_callback_type}:{message_id}:{user_telegram_id}:{chat_id}",
        )
        inline_keyboard.add(button)
        self.bot.edit_message_text(
            chat_id=chat_id,
            message_id=int(message_id),
            text=text,
            reply_markup=inline_keyboard,
            parse_mode="html",
        )

    def callback_cash_savings_values_process(self, callback_query):
        (
            amount,
            method,
            saving_callback_type,
            message_id,
            user_telegram_id,
            chat_id,
        ) = callback_query.data.split(":")
        saving_type = getattr(CashSaving.SavingType, saving_callback_type)
        try:
            user_cash_saving = CashSaving.objects.get(
                user__telegram_id=user_telegram_id, saving_type=saving_type
            )
            text = "Value of {saving_type} was changed to {user_cash_saving}$"
        except cash_savings.models.CashSaving.DoesNotExist:
            user = TelegramUser.objects.get(telegram_id=user_telegram_id)
            user_cash_saving = CashSaving.objects.create(
                user=user, saving_type=saving_type, amount=0
            )
            text = "{saving_type} was created with {user_cash_saving}$"
        user_cash_saving.amount += float(amount) if method == "add" else -float(amount)
        user_cash_saving.save(update_fields=["amount"])
        self.bot.answer_callback_query(
            callback_query_id=callback_query.id,
            text=text.format(
                saving_type=saving_type, user_cash_saving=user_cash_saving.amount
            ),
            show_alert=False,
        )
        self.cash_saving_type_process(
            f"{saving_callback_type}:{user_telegram_id}:{chat_id}:{message_id}"
        )

    def echo_message_process(self, message):
        text = "Wrong command!\nTo see list cash savings, use <b>/cash_savings</b> command."
        self.bot.reply_to(message=message, text=text, parse_mode="html")
