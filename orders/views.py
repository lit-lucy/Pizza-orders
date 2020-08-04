from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import *

# Create your views here.
def index(request):

    context = {

        "food_types": FoodType.objects.all(),
        
    }
    return render(request, "orders/index.html", context)

def food_modifications(request, food_id):
    try:
        food = Food.objects.get(id=food_id)
    except Food.DoesNotExist:
        raise Http404("Dish does not exist")

    context = {
        "food": food,
        "range": range(food.number_of_extras),
    }

    return render(request, "orders/food.html", context)

def add_to_order(request, food_id):
    food = get_object_or_404(Food, pk=food_id)
    # Add try and except 
    base_price = food.baseprice_set.get(size=request.POST['size']).price
    extra_price = 0

    extras = request.POST.getlist('extras')
    for extra in extras:
        if extra != '0':
            extra_price += Extra.objects.get(pk=int(extra)).extraprice_set.get(food=food_id).price


    context = {
        "price": base_price + extra_price,
        "food": food,
        "extras": extras,
        "base_price": food.baseprice_set.get(size=request.POST['size']),

    } 

    return render(request, "orders/check.html", context)
