from django.http import HttpResponse, Http404
from django.shortcuts import render

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
        "food": food
    }

    return render(request, "orders/food.html", context)