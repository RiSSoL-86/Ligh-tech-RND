# Generated by Django 5.0.8 on 2024-08-07 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(help_text='Название банка, в котором открыт счёт', max_length=255, verbose_name='Название банка')),
                ('account_number', models.CharField(help_text='Номер банковского счёта', max_length=255, unique=True, verbose_name='Номер счёта')),
                ('balance_amount', models.DecimalField(decimal_places=2, help_text='Текущий баланс на счёте', max_digits=15, verbose_name='Баланс на счёте')),
                ('currency', models.CharField(default='RUB', help_text='Валюта счёта', max_length=10, verbose_name='Валюта')),
                ('created_dt', models.DateTimeField(auto_now_add=True, help_text='Дата создания банковского баланса пользователя', verbose_name='Дата создания')),
                ('updated_dt', models.DateTimeField(auto_now=True, help_text='Дата изменений данных банковского баланса пользователя', verbose_name='Дата изменений')),
            ],
            options={
                'verbose_name': 'Баланс банковского счёта',
                'verbose_name_plural': 'Балансы банковских счетов',
                'ordering': ('user', 'bank_name', 'account_number'),
            },
        ),
    ]
