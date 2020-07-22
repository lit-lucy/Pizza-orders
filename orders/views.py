from django.http import HttpResponse
from django.shortcuts import render

from .models import Size

# Create your views here.
def index(request):
    context = {
        "sizes": Size.objects.all()
    }
    return render(request, "orders/index.html", context)
