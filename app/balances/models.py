from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator

from users.models import User


class Balance(models.Model):
    """Модель баланса банковского счёта."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='balances',
        verbose_name='Пользователь',
        help_text='Пользователь, к которому относится этот баланс'
    )
    bank_name = models.CharField(
        max_length=255,
        verbose_name='Название банка',
        help_text='Название банка, в котором открыт счёт'
    )
    account_number = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Номер счёта',
        help_text='Номер банковского счёта'
    )
    balance_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Баланс на счёте',
        help_text='Текущий баланс на счёте'
    )
    currency = models.CharField(
        max_length=10,
        default='RUB',
        verbose_name='Валюта',
        help_text='Валюта счёта'
    )
    created_dt = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
        help_text='Дата создания банковского баланса пользователя'
    )
    updated_dt = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменений',
        help_text='Дата изменений данных банковского баланса пользователя'
    )

    class Meta:
        ordering = ('user', 'bank_name', 'account_number')
        verbose_name = 'Баланс банковского счёта'
        verbose_name_plural = 'Балансы банковских счетов'

    def __str__(self):
        return f"{self.user.username} - {self.bank_name} ({self.account_number})"
