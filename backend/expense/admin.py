from django.contrib import admin

from .models import Expense


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ["trip", "category", "amount", "currency"]


admin.site.register(Expense, ExpenseAdmin)
