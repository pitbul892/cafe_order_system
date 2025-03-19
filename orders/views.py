from django.shortcuts import render
from .models import Order
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
# Create your views here.

def paginator(page_number, post_list):
    paginator = Paginator(post_list, 5)
    return paginator.get_page(page_number)

def index(request):
    template = ("order/index.html",)
    order_list = Order.objects.all()
    page_obj = paginator(request.GET.get("page"), order_list)
    context = {"page_obj": page_obj}
    return render(request, template, context)

def order_detail(request, order_id):
    template = ("order/detail.html",)
    order = get_object_or_404(Order, pk=order_id)
   
    context = {"order": order}
    return render(request, template, context)