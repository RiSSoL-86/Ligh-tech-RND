from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator

from balances.models import Balance


class Operation(models.Model):
    """Модель операций с балансом банковского счёта пользователя."""
    OPERATION_TYPE_CHOICES = [
        ('withdrawal', 'Снятие'),
        ('transfer', 'Пополнение'),
        ('fee', 'Оплата'),
    ]
    balance = models.ForeignKey(
        Balance,
        on_delete=models.CASCADE,
        related_name='operations',
        verbose_name='Банковский баланс',
        help_text='Операции с банковским балансом пользователя'
    )
    operation_type = models.CharField(
        max_length=50,
        choices=OPERATION_TYPE_CHOICES,
        verbose_name='Тип операции',
        help_text='Тип операции с балансом'
    )
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Сумма',
        help_text='Сумма операции'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
        help_text='Описание операции'
    )
    created_dt = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
        help_text='Дата создания операции с банковским балансом пользователя'
    )
    updated_dt = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата внесений изменений',
        help_text='Дата изменений данных операции с банковским балансом пользователя'
    )

    def get_operation_type_display(self):
        return dict(self.OPERATION_TYPE_CHOICES).get(self.operation_type, self.operation_type)

    class Meta:
        ordering = ('-created_dt',)
        verbose_name = 'Операция'
        verbose_name_plural = 'Операции'

    def __str__(self):
        return f"Счёт: №{self.balance.account_number}. Операция [{self.get_operation_type_display()}] на сумму - {self.amount} руб. Oт {self.created_dt.strftime('%d-%m-%Y %H:%M:%S')}"
