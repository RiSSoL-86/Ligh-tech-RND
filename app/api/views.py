from decimal import Decimal, InvalidOperation

from djoser.views import UserViewSet
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions

from .filters import BalanceFilter, OperationFilter
from .serializers import (
    BalanceAmountUpdateSerializer,
    BalanceWithRelationsSerializer,
    UserWithRelationsSerializer,
    OperationWithRelationsSerializer
)
from users.models import User
from balances.models import Balance
from operations.models import Operation


class CustomUserViewSet(UserViewSet):
    """Вьюсет для модели Пользователя."""
    queryset = User.objects.all()
    serializer_class = UserWithRelationsSerializer
    http_method_names = ['get', 'post']
    permission_classes = [permissions.AllowAny]


class BalancesViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Баланса банковского счёта."""
    queryset = Balance.objects.all()
    serializer_class = BalanceWithRelationsSerializer
    http_method_names = ['get', 'post', 'patch']
    filterset_class = BalanceFilter

    def partial_update(self, request, *args, **kwargs):
        """Обработка пополнения баланса банковского счёта пользователя.
           Источником может быть наличка (т.е. без указания счёта списания)
           или же с указанием счёт для списания денежных средств."""
        balance_id = kwargs.get('pk')
        try:
            balance = Balance.objects.get(id=balance_id)
        except Balance.DoesNotExist:
            return Response({'detail': 'Balance not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BalanceAmountUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data.get('amount')
        try:
            amount = Decimal(amount)
        except (ValueError, InvalidOperation):
            return Response({'detail': 'Invalid amount value.'}, status=status.HTTP_400_BAD_REQUEST)
        transfer_balance_id = serializer.validated_data.get('transfer_balance_id', None)
        # Проверка, что идентификаторы счета пополнения и списания не совпадают
        if transfer_balance_id:
            if int(transfer_balance_id) == balance.id:
                return Response({'detail': 'Cannot transfer funds to the same account.'}, status=status.HTTP_400_BAD_REQUEST)
        if transfer_balance_id:  # обработка случая если указали счёт списания средств
            try:
                transfer_balance = Balance.objects.get(id=transfer_balance_id)
            except Balance.DoesNotExist:
                return Response({'detail': 'Transfer balance not found.'}, status=status.HTTP_404_NOT_FOUND)
            if request.user != transfer_balance.user:
                return Response({'detail': 'You do not have permission to edit the transfer balance.'}, status=status.HTTP_403_FORBIDDEN)
            # Проверка достаточности средств для списания
            if transfer_balance.balance_amount < amount:
                return Response({'detail': 'Insufficient funds.'}, status=status.HTTP_400_BAD_REQUEST)
            # Выполнение перевода средств
            transfer_balance.balance_amount -= amount
            balance.balance_amount += amount
            # Сохранение изменений
            balance.save()
            transfer_balance.save()
            # Создание записей в модели Operation
            Operation.objects.create(
                balance=transfer_balance,
                operation_type='transfer',
                amount=amount,
                description=f'Перевод средств на счет №{balance.account_number} '
                            f'[{balance.bank_name}] для {balance.user.last_name} {balance.user.first_name}'
            )
            Operation.objects.create(
                balance=balance,
                operation_type='withdrawal',
                amount=amount,
                description=f'Получены средства со счета №{transfer_balance.account_number} '
                            f'[{transfer_balance.bank_name}] от {transfer_balance.user.last_name} {transfer_balance.user.first_name}'
            )
        else:
            # Пополнение счета наличкой
            balance.balance_amount += amount
            balance.save()
            # Создание записи в модели Operation
            Operation.objects.create(
                balance=balance,
                operation_type='transfer',
                amount=amount,
                description='Ваш баланс пополнен'
            )
        return super().partial_update(request, *args, **kwargs)


class OperationsViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Операций с балансом банковского счёта пользователя."""
    queryset = Operation.objects.all()
    serializer_class = OperationWithRelationsSerializer
    http_method_names = ['get']
    filterset_class = OperationFilter

    def get_queryset(self):
        """Доступ к просмотру операциий по банковскому счёту имеет только
           собственник баланса."""
        user = self.request.user
        return Operation.objects.filter(balance__user=user)
