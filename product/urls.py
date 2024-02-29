from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list),
    path('products/<int:product_id>/lessons/', views.lesson_list, name='lesson_list'),
]