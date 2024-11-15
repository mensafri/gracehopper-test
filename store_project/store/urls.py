from django.urls import path
from . import views

urlpatterns = [
    path('api/categories/', views.category_list, name='category-list'),
    path('api/products/', views.product_list, name='product-list'),
]
