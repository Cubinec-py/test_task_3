from django.contrib import admin
from cash_savings.models import CashSaving


@admin.register(CashSaving)
class CashSavingAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "saving_type",
        "amount",
    ]
    list_filter = ["saving_type"]
    search_fields = ["user__username"]

    autocomplete_fields = ["user"]
