from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:food_id>", views.food_modifications, name="food_modifications"),

]
