from django.contrib import admin

from .models import User
from balances.models import Balance


class BalancesInline(admin.TabularInline):
    """Настройка отображения банковского счёта."""
    model = Balance
    min_num = 1


class UserAdmin(admin.ModelAdmin):
    """Настройка Админки-Пользователей."""
    @admin.display(description='Банковские счета пользователя')
    def get_balances(self, obj):
        """Функция для корректного отображения банковских счётов пользователя в
           list_display Админке-Пользователей."""
        balances = Balance.objects.filter(user=obj.id)
        return [f'{i.bank_name}: {i.account_number}' for i in balances]

    list_display = (
        'id',
        'username',
        'last_name',
        'first_name',
        'email',
        'get_balances'
    )
    search_fields = ('username', 'first_name', 'email')
    list_filter = ('username', 'first_name', 'email')


admin.site.register(User, UserAdmin)
