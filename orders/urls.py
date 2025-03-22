from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name='index'),
    path('orders/<int:order_id>/', views.order_detail, name="order_detail"),
    path('orders/<int:order_id>/delete/', views.order_delete,
         name="order_delete"),
    path('orders/create/', views.OrderCreateView.as_view(),
         name="order_create"),
    path('orders/revenue/', views.revenue_for_shift, name="revenue")
]
