from rest_framework.test import APITestCase
from rest_framework import status
from django.core.cache import cache
from .models import Category, Product

class StoreAPITest(APITestCase):

    def setUp(self):
        # Membuat data awal untuk tes
        self.category = Category.objects.create(name="Electronics", description="Gadgets and devices")
        self.product = Product.objects.create(
            name="Smartphone",
            description="Latest smartphone",
            price=299.99,
            category=self.category
        )
        print("\n[SetUp] Created initial test data.")

    def test_list_categories(self):
        print("\n[Test] Testing GET /api/categories/")
        response = self.client.get("/api/categories/")
        print(f"[Result] Status Code: {response.status_code}")
        print(f"[Result] Response Data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_category(self):
        print("\n[Test] Testing POST /api/categories/")
        data = {"name": "Furniture", "description": "Home and office furniture"}
        response = self.client.post("/api/categories/", data)
        print(f"[Result] Status Code: {response.status_code}")
        print(f"[Result] Response Data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)

    def test_category_detail(self):
        print("\n[Test] Testing GET /api/categories/{id}/")
        response = self.client.get(f"/api/categories/{self.category.id}/")
        print(f"[Result] Status Code: {response.status_code}")
        print(f"[Result] Response Data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Electronics")

    def test_update_category(self):
        print("\n[Test] Testing PUT /api/categories/{id}/")
        data = {"name": "Updated Category", "description": "Updated description"}
        response = self.client.put(f"/api/categories/{self.category.id}/", data)
        print(f"[Result] Status Code: {response.status_code}")
        print(f"[Result] Response Data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Updated Category")

    def test_delete_category(self):
        print("\n[Test] Testing DELETE /api/categories/{id}/")
        response = self.client.delete(f"/api/categories/{self.category.id}/")
        print(f"[Result] Status Code: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)

    def test_list_products_with_filter(self):
        print("\n[Test] Testing GET /api/products/ with filters")
        response = self.client.get("/api/products/", {"category": "Electronics"})
        print(f"[Result] Status Code: {response.status_code}")
        print(f"[Result] Response Data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Smartphone", str(response.data))

    def test_product_detail(self):
        print("\n[Test] Testing GET /api/products/{id}/")
        response = self.client.get(f"/api/products/{self.product.id}/")
        print(f"[Result] Status Code: {response.status_code}")
        print(f"[Result] Response Data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Smartphone")

    def test_update_product(self):
        print("\n[Test] Testing PUT /api/products/{id}/")
        data = {
            "name": "Updated Product",
            "description": "Updated description",
            "price": 500.00,
            "category": self.category.id
        }
        response = self.client.put(f"/api/products/{self.product.id}/", data)
        print(f"[Result] Status Code: {response.status_code}")
        print(f"[Result] Response Data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Updated Product")

    def test_delete_product(self):
        print("\n[Test] Testing DELETE /api/products/{id}/")
        response = self.client.delete(f"/api/products/{self.product.id}/")
        print(f"[Result] Status Code: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)
