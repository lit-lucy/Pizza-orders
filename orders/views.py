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

    return HttpResponse('done')
