from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:subtype_id>', views.food_modifications, name='food_modifications'),
    path('<int:subtype_id>/add_to_order/', views.add_to_order, name='add_to_order'),
    path('last_added_item/', views.last_added_item, name='last_added_item'),
    path('shopping_cart/', views.shopping_cart, name='shopping_cart'),
    path('<int:item_id>/delete_from_order/', views.delete_from_order, name='delete_from_order'),
    path('<int:item_id>/change_quantity/', views.change_quantity, name='change_quantity'),
    path('confirm_order/', views.confirm_order, name='confirm_order'),
    path('order_status/', views.order_status, name='order_status'),

]
