from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:food_id>", views.food_modifications, name="food_modifications"),
    path('<int:food_id>/add_to_order/', views.add_to_order, name='add_to_order'),

]
