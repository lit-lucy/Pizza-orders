from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone

from .models import *
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    context = {
        "food_types": FoodType.objects.all(),
    }
    return render(request, "orders/index.html", context)

def food_modifications(request, subtype_id):
    try:
        subtype = Subtype.objects.get(id=subtype_id)
    except Subtype.DoesNotExist:
        raise Http404("Dish does not exist")

    context = {
        "subtype": subtype,
        "range": range(subtype.number_of_extras),
    }

    return render(request, "orders/food.html", context)

def add_to_order(request, subtype_id):
    # Get dish and it's size
    subtype = get_object_or_404(Subtype, pk=subtype_id)
    dish = subtype.dish_set.get(size=request.POST['size'])

    # Compile an order
    # Test user for now, then add user_id 
    user = User.objects.get(pk=2)
    # Status 'in shopping cart'
    status = Status.objects.get(pk=1)
    delivery = DeliveryType.objects.get(pk=1)

    # Get(if order with such session exists) or create order
    order, created = Order.objects.get_or_create(session=request.session.session_key,
            defaults={'status': status,
            'user': user,
            'time_created': timezone.now(),
            'delivery_type': delivery,
            'is_paid': False

            })
    # Add item to an order    
    order_item = OrderItem(order=order, dish=dish, price=dish.price)
    order_item.save()

    extras = request.POST.getlist('extras')
    for extra_id in extras:
        if extra_id != '0':
            extra = ExtraType.objects.get(pk=int(extra_id)).extra_set.get(subtype=subtype_id)
            order_extra = OrderItemExtra(order_item=order_item, extra=extra, price=extra.price)
            order_extra.save()
            

    context = {
        
        "dish": subtype,
        "extras": extras,
        "dish_price": subtype.dish_set.get(size=request.POST['size']),

    } 

    return redirect("order_summary")

def order_summary(request):
    context = {
    "data": "added to orders",

    }
    return render(request, "orders/check.html", context)
