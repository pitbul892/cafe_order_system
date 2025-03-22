from django.urls import path

from .views import (OrderDetailAPIView, OrderListCreateAPIView,
                    RevenueForShiftAPIView)

app_name = 'api'

urlpatterns = [
    path('orders/', OrderListCreateAPIView.as_view(),
         name='api_order_list_create'),
    path('orders/<int:pk>/', OrderDetailAPIView.as_view(),
         name='api_order_detiail'),
    path('revenue/', RevenueForShiftAPIView.as_view(), name='api_revenue'),
]
