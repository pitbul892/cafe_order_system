from rest_framework import serializers

from orders.models import Dish, Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    """Сериалайзер блюда для чтения."""

    class Meta:
        model = Dish
        fields = '__all__'


class OrderItemCreateSerializer(serializers.ModelSerializer):
    """Сериалайзер блюда для создания."""

    id = serializers.IntegerField()

    class Meta:
        model = OrderItem
        fields = ('id', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    """Сериалайзер заказа для чтения."""

    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'


class OrderUpdateSerializer(serializers.ModelSerializer):
    """Сериалайзер заказа для изменения статуса."""

    class Meta:
        model = Order
        fields = ['id', 'status']


class OrderCreateSerializer(serializers.ModelSerializer):
    """Сериалайзер заказа для создания."""

    items = OrderItemCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'table_number', 'items']

    def validate(self, data):
        """Вадидация блюд."""
        items_data = data.get('items')
        items = []
        if not items_data:
            raise serializers.ValidationError('Добавьте блюда.')

        for item in items_data:
            try:
                Dish.objects.get(pk=item['id'])
            except Dish.DoesNotExist:
                raise serializers.ValidationError(
                    'Такого блюда не существует.')
            if item in items:
                raise serializers.ValidationError(
                    f'{Dish.objects.get(pk=item["id"])} уже есть.'
                )
            quantity = item.get('quantity')
            if not quantity:
                raise serializers.ValidationError(
                    'Колиство блюд не может быть 0.')
            items.append(item)
        return data

    def create(self, validated_data):
        """Создание."""
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item in items_data:
            OrderItem.objects.create(
                dish=Dish.objects.get(pk=item['id']),
                order=order,
                quantity=item['quantity']
            )
        return order

    def to_representation(self, instance):
        """Переопределение."""
        serializer = OrderSerializer(
            instance, context={'request': self.context['request']}
        )
        return serializer.data
