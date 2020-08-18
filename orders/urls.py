from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:subtype_id>', views.food_modifications, name='food_modifications'),
    path('<int:subtype_id>/add_to_order/', views.add_to_order, name='add_to_order'),
    path('<int:order_id>/last_added_item/', views.last_added_item, name='last_added_item'),
    path('shopping_cart/', views.shopping_cart, name='shopping_cart'),

]
