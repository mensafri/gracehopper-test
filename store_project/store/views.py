from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

@api_view(['GET', 'POST'])
def category_list(request):
    if request.method == 'GET':
        categories = cache.get('store:categories')
        if not categories:
            categories = list(Category.objects.all())
            cache.set('store:categories', categories, timeout=300)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete('store:categories')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        filters = {}
        category = request.query_params.get('category')
        price_min = request.query_params.get('price_min')
        price_max = request.query_params.get('price_max')

        if category:
            filters['category__name__icontains'] = category
        if price_min:
            filters['price__gte'] = price_min
        if price_max:
            filters['price__lte'] = price_max

        products = cache.get('store:products')
        if not products:
            products = list(Product.objects.filter(**filters))
            cache.set('store:products', products, timeout=300)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete('store:products')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
