from rest_framework.test import APITestCase
from rest_framework import status
from django.core.cache import cache
from .models import Category, Product

class StoreAPITest(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Smartphone",
            description="Latest smartphone",
            price=299.99,
            category=self.category
        )
        print("\nSetUp: Created initial test data.")

    def test_list_categories(self):
        response = self.client.get("/api/categories/")
        if response.status_code == status.HTTP_200_OK:
            print("Test `test_list_categories`: SUCCESS - Categories listed successfully.")
            print("Response Data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_category(self):
        data = {"name": "Furniture", "description": "Home and office furniture"}
        response = self.client.post("/api/categories/", data)
        if response.status_code == status.HTTP_201_CREATED:
            print("Test `test_create_category`: SUCCESS - Category created successfully.")
            print("Created Category Data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)

    def test_cache_categories(self):
        cache.clear()
        self.client.get("/api/categories/")
        with self.assertNumQueries(0):
            response = self.client.get("/api/categories/")
            if response.status_code == status.HTTP_200_OK:
                print("Test `test_cache_categories`: SUCCESS - Categories retrieved from cache.")
                print("Response Data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_products_with_filter(self):
        response = self.client.get("/api/products/", {"category": "Electronics"})
        if response.status_code == status.HTTP_200_OK:
            print("Test `test_list_products_with_filter`: SUCCESS - Products filtered successfully.")
            print("Filtered Products Data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Smartphone", str(response.data))

    def test_cache_invalidation_on_create(self):
        cache.set("store:categories", "dummy_data", timeout=300)
        response = self.client.post("/api/categories/", {"name": "Books", "description": "Educational books"})
        if cache.get("store:categories") is None:
            print("Test `test_cache_invalidation_on_create`: SUCCESS - Cache invalidated successfully.")
        else:
            print("Test `test_cache_invalidation_on_create`: FAILURE - Cache not invalidated.")
        self.assertIsNone(cache.get("store:categories"))
