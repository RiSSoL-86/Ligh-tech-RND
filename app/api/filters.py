from django_filters import rest_framework

from operations.models import Operation
from balances.models import Balance


class BalanceFilter(rest_framework.FilterSet):
    user_id = rest_framework.NumberFilter(field_name='user__id')

    class Meta:
        model = Balance
        fields = ['user_id']


class OperationFilter(rest_framework.FilterSet):
    balance_id = rest_framework.NumberFilter(field_name='balance__id')

    class Meta:
        model = Operation
        fields = ['balance_id']
