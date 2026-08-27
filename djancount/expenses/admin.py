from django.contrib import admin
from .models import Event, Expense


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
    filter_horizontal = ("participants",)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("title", "amount", "payer", "event", "date")
    list_filter = ("event", "payer")
    search_fields = ("title",)