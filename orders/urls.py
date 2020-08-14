from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:subtype_id>', views.food_modifications, name='food_modifications'),
    path('<int:subtype_id>/add_to_order/', views.add_to_order, name='add_to_order'),
    path('<int:order_id>/order_summary/', views.order_summary, name='order_summary'),
    path('shopping_cart/', views.shopping_cart, name='shopping_cart'),

]
