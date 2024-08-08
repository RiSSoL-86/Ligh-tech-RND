from django.contrib import admin

from .models import Balance
from operations.models import Operation


class OperationsInline(admin.TabularInline):
    """Настройка отображения операций по банковскому счёту."""
    model = Operation
    min_num = 1


class BalanceAdmin(admin.ModelAdmin):
    """Настройка Админки-Баланса."""
    @admin.display(description='Фамилия пользователя')
    def user_last_name(self, obj):
        """Возвращает фамилию пользователя."""
        return obj.user.last_name

    @admin.display(description='Имя пользователя')
    def user_first_name(self, obj):
        """Возвращает имя пользователя."""
        return obj.user.first_name

    list_display = (
        'id',
        'user_last_name',
        'user_first_name',
        'bank_name',
        'account_number',
        'balance_amount',
        'currency',
    )
    search_fields = ('user__first_name', 'user__last_name', 'bank_name')
    list_filter = ('user__first_name', 'user__last_name', 'bank_name', 'currency')


admin.site.register(Balance, BalanceAdmin)
