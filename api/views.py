from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

import constants as c
from orders.models import Order

from .serializers import (OrderCreateSerializer, OrderSerializer,
                          OrderUpdateSerializer)

today = timezone.now().date()


class OrderListCreateAPIView(generics.ListCreateAPIView):
    """Функция для получения списка и создания."""

    queryset = Order.objects.filter(pub_date__date=today)

    def get_serializer_class(self):
        """Разные сериализаторы для GET и POST."""
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderSerializer


class OrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Функция для получения по id, частичного изменения и удаления."""

    queryset = Order.objects.all()
    serializer_class = OrderUpdateSerializer

    def partial_update(self, request, *args, **kwargs):
        """Разрешаем менять только статус заказа."""
        order = self.get_object()
        allowed_statuses = [status[0] for status in c.STATUS_CHOICES]

        new_status = request.data.get('status')

        if new_status not in allowed_statuses:
            return Response(
                {'error': f'Статус может быть только {allowed_statuses}.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = new_status
        order.save()

        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)


class RevenueForShiftAPIView(APIView):
    """Функция для получения выручки за смену."""

    def get(self, request):
        """Получение выручки."""
        orders = Order.objects.filter(pub_date__date=today, status='Paid')
        total_revenue = sum(order.total_price for order in orders)
        total_orders = orders.count()
        return Response(
            {'total_revenue': total_revenue,
             'total_orders': total_orders},
            status=status.HTTP_200_OK)
