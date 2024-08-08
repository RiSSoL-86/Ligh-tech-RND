from django.contrib import admin
from .models import Operation


class OperationAdmin(admin.ModelAdmin):
    """Настройка Админки-Операций."""
    @admin.display(description='Фамилия пользователя')
    def user_last_name(self, obj):
        """Возвращает фамилию пользователя."""
        return obj.balance.user.last_name

    @admin.display(description='Имя пользователя')
    def user_first_name(self, obj):
        """Возвращает имя пользователя."""
        return obj.balance.user.first_name

    @admin.display(description='Банковский счёт')
    def balance_info(self, obj):
        """Возвращает информацию по банковскому счёту."""
        return f'{obj.balance.bank_name}: {obj.balance.account_number}'

    list_display = (
        'id',
        'user_last_name',
        'user_first_name',
        'balance_info',
        'operation_type',
        'amount',
        'description',
    )
    search_fields = ('balance__user__first_name', 'balance__user__last_name', 'balance__bank_name')
    list_filter = ('balance__user__first_name', 'balance__user__last_name', 'balance__bank_name', 'operation_type')


admin.site.register(Operation, OperationAdmin)
