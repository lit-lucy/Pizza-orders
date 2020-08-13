from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:subtype_id>", views.food_modifications, name="food_modifications"),
    path('<int:subtype_id>/add_to_order/', views.add_to_order, name='add_to_order'),
    path('order_summary', views.order_summary, name='order_summary'),

]
