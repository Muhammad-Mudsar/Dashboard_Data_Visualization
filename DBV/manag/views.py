"""
Module: store.views

Contains Django views for managing items, profiles,
and deliveries in the store application.

Classes handle product listing, creation, updating,
deletion, and delivery management.
The module integrates with Django's authentication
and querying functionalities.
"""
from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.

# def index(request):
    # return HttpResponse(request, "Helow world")


from datetime import timedelta
from django.db.models import Sum, Count
from django.http import JsonResponse

from django.utils import timezone
from django.utils.dateparse import parse_date
from .models import Order,Product

def get_date_range(start=None, end=None):
    """Return (start_datetime, end_datetime) defaulting to last 30 days."""
    today = timezone.now().date()
    if not end:
        end = today
    else:
        end = parse_date(end) or today
    if not start:
        start = end - timedelta(days=29)
    else:
        start = parse_date(start) or (end - timedelta(days=29))

    start_dt = timezone.make_aware(timezone.datetime.combine(start, timezone.datetime.min.time()))
    end_dt = timezone.make_aware(timezone.datetime.combine(end, timezone.datetime.max.time()))
    return start_dt, end_dt

def get_dashboard_stats(start, end):
    """Aggregate stats for given date range."""
    orders = Order.objects.filter(order_date__range=[start, end])
    producs_today= Product.objects.count()

    # Stat cards
    total_revenue = orders.aggregate(Sum('total_price'))['total_price__sum'] or 0
    total_orders = orders.count()
    avg_order_value = total_revenue / total_orders if total_orders else 0
    unique_products = orders.values('product').distinct().count()

    # Revenue by product (bar chart)
    product_revenue = list(
        orders.values('product__name')
        .annotate(revenue=Sum('total_price'))
        .order_by('-revenue')[:10]
    )

    # Revenue over time (line chart)
    daily_revenue = list(
        orders.values('order_date__date')
        .annotate(revenue=Sum('total_price'))
        .order_by('order_date__date')
    )

    # Revenue by category (pie/donut)
    category_revenue = list(
        orders.values('product__category__name')
        .annotate(revenue=Sum('total_price'))
        .order_by('-revenue')
    )

    return {
        'stat_cards': {
            'total_revenue': float(total_revenue),
            'total_orders': total_orders,
            'avg_order_value': float(avg_order_value),
            'unique_products': unique_products,
        },
        'product_revenue': {
            'labels': [item['product__name'] for item in product_revenue],
            'values': [float(item['revenue']) for item in product_revenue],
        },
        'daily_revenue': {
            'labels': [item['order_date__date'].strftime('%Y-%m-%d') for item in daily_revenue],
            'values': [float(item['revenue']) for item in daily_revenue],
        },
        'category_revenue': {
            'labels': [item['product__category__name'] for item in category_revenue],
            'values': [float(item['revenue']) for item in category_revenue],
        },
    }

def dashboard(request):
    return render(request, 'manag/dashboard.html')

def dashboard_data(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    start_dt, end_dt = get_date_range(start, end)
    data = get_dashboard_stats(start_dt, end_dt)

    return JsonResponse(data)

def product_list_data(request):
    q = request.GET.get('q', '').strip()
    # No date filter – lists all products with overall sales
    orders = Order.objects.all()
    if q:
        orders = orders.filter(product__name__icontains=q)

    product_list = list(
        orders.values(
            'product__id',
            'product__name',
            'product__category__name',
            'product__price'
        )
        .annotate(
            total_quantity=Sum('quantity'),
            total_revenue=Sum('total_price')
        )
        .order_by('product__name')
    )
    return JsonResponse({'products': product_list})