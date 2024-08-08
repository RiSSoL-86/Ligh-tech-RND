from rest_framework import serializers

from app.settings import DEFAULT_PAGES_LIMIT
from users.models import User
from balances.models import Balance
from operations.models import Operation


class BaseBalanceSerializer(serializers.ModelSerializer):
    """Вспомогательный сериализатор для корректного отображения балансов
       банковского счёта пользователя."""

    class Meta:
        model = Balance
        fields = (
            'id',
            'bank_name',
            'account_number',
            'currency'
        )


class UserWithRelationsSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя."""
    balances = serializers.SerializerMethodField(read_only=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'last_name',
            'first_name',
            'email',
            'balances',
            'password',
        )

    def create(self, validated_data):
        """Сохранение хэшированного пароля пользователя."""
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def get_balances(self, obj):
        """Список балансов банковского счёта пользователя."""
        request = self.context.get('request')
        limit = request.GET.get('balances_limit', DEFAULT_PAGES_LIMIT)
        try:
            limit = int(limit)
        except ValueError:
            pass
        return BaseBalanceSerializer(
            Balance.objects.filter(user=obj.id)[:limit],
            many=True
        ).data


class BaseUserSerializer(serializers.ModelSerializer):
    """Вспомогательный сериализатор для корректного отображения пользователя в
       балансе банковского счёта."""

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'last_name',
            'first_name',
            'email',
        )


class BalanceWithRelationsSerializer(serializers.ModelSerializer):
    """Сериализатор для баланса банковского счёта пользователя."""
    user = BaseUserSerializer(read_only=True)

    class Meta:
        model = Balance
        fields = (
            'id',
            'user',
            'bank_name',
            'account_number',
            'balance_amount',
            'currency',
        )

    def create(self, validated_data):
        """Устанавливает текущего пользователя как владельца баланса при
           создании счёта."""
        request = self.context.get('request')
        user = request.user
        return Balance.objects.create(user=user, **validated_data)

    def to_representation(self, instance):
        """Отображает balance_amount только для владельца счета, остальным
           пользователям данная информация недоступна."""
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request.user != instance.user:
            representation.pop('balance_amount')
        return representation


class BalanceAmountUpdateSerializer(serializers.Serializer):
    """Сериализатор для пополнения суммы баланса банковского счёта."""
    amount = serializers.DecimalField(max_digits=20, decimal_places=2)
    transfer_balance_id = serializers.IntegerField(required=False, allow_null=True)

    def validate_amount(self, value):
        """Проверка валидности суммы."""
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value


class OperationWithRelationsSerializer(serializers.ModelSerializer):
    """Сериализатор для операций с балансом банковского счёта пользователя."""
    balance = BaseBalanceSerializer(read_only=True)
    operation_type = serializers.SerializerMethodField()

    class Meta:
        model = Operation
        fields = (
            'id',
            'balance',
            'operation_type',
            'amount',
            'description',
        )

    def get_operation_type(self, obj):
        """Возвращает описание типа операции."""
        return dict(Operation.OPERATION_TYPE_CHOICES).get(obj.operation_type, obj.operation_type)
