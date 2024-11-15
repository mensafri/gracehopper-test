from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_overview, name='api-overview'),

    path('api/categories/', views.category_list, name='category-list'),
    path('api/categories/<int:pk>/', views.category_detail, name='category-detail'),

    path('api/products/', views.product_list, name='product-list'),
    path('api/products/<int:pk>/', views.product_detail, name='product-detail'),
]
