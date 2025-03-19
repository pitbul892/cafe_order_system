from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.index, name='index'),
    path('orders/<int:order_id>/', views.order_detail, name="order_detail")
]