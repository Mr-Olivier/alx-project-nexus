



# apps/products/views.py

"""
Essential E-commerce Views

Only the most commonly used APIs for e-commerce.
"""

from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema

from .permissions import IsAdminUser
from .models import Product, Category
from .serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
    ProductCreateUpdateSerializer,
    CategoryListSerializer,
    CategoryDetailSerializer,
    CategoryCreateUpdateSerializer
)
from .filters import ProductFilter
from .pagination import ProductPagination


# ========================================================================
# PRODUCT APIS
# ========================================================================

class ProductListCreateView(generics.ListCreateAPIView):
    """
    List all products with filtering and search OR Create new product
    """
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'sku']
    ordering_fields = ['name', 'price', 'created_at']
    ordering = ['-created_at']
    pagination_class = ProductPagination
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateUpdateSerializer
        return ProductListSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdminUser()]
        return [AllowAny()]
    
    def get_queryset(self):
        if self.request.method == 'GET':
            return Product.objects.filter(is_active=True).select_related('category')
        return Product.objects.all()

    @extend_schema(
        summary="List all products",
        description="Get paginated list of products. Filter by category, price range, search by name/description/SKU. Public access.",
        tags=['Products']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Create new product",
        description="Create a new product with name, description, price, category. Requires admin authentication.",
        tags=['Products']
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ProductDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    Get product details OR Update product OR Delete product
    """
    
    lookup_field = 'pk'
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductDetailSerializer
        return ProductCreateUpdateSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminUser()]
    
    def get_queryset(self):
        if self.request.method == 'GET':
            return Product.objects.filter(is_active=True).select_related('category')
        return Product.objects.all()
    
    def get_object(self):
        lookup_value = self.kwargs.get('pk')
        
        # Try UUID first, then slug
        try:
            if len(lookup_value) == 36 and '-' in lookup_value:
                return get_object_or_404(self.get_queryset(), id=lookup_value)
            else:
                return get_object_or_404(self.get_queryset(), slug=lookup_value)
        except:
            return get_object_or_404(Product, id=None)

    @extend_schema(
        summary="Get product details",
        description="Retrieve complete product information including images, category, pricing, and stock details. Use product ID or slug.",
        tags=['Products']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update product",
        description="Update product information like price, stock, description. Requires admin authentication.",
        tags=['Products']
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Partial update product",
        description="Update specific product fields like price or stock quantity. Requires admin authentication.",
        tags=['Products']
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary="Delete product",
        description="Soft delete product (sets is_active=False). Product will be hidden from public listings. Requires admin authentication.",
        tags=['Products']
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


# ========================================================================
# CATEGORY APIS  
# ========================================================================

class CategoryListCreateView(generics.ListCreateAPIView):
    """
    List all categories OR Create new category
    """
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering = ['name']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CategoryCreateUpdateSerializer
        return CategoryListSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdminUser()]
        return [AllowAny()]
    
    def get_queryset(self):
        if self.request.method == 'GET':
            return Category.objects.filter(is_active=True)
        return Category.objects.all()

    @extend_schema(
        summary="List all categories",
        description="Get list of all product categories with product counts. Search by name or description. Public access.",
        tags=['Categories']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Create new category",
        description="Create a new product category with name and description. Used to organize products. Requires admin authentication.",
        tags=['Categories']
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CategoryDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    Get category details OR Update category OR Delete category
    """
    
    lookup_field = 'pk'
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CategoryDetailSerializer
        return CategoryCreateUpdateSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminUser()]
    
    def get_queryset(self):
        if self.request.method == 'GET':
            return Category.objects.filter(is_active=True)
        return Category.objects.all()
    
    def get_object(self):
        lookup_value = self.kwargs.get('pk')
        
        # Try UUID first, then slug
        try:
            if len(lookup_value) == 36 and '-' in lookup_value:
                return get_object_or_404(self.get_queryset(), id=lookup_value)
            else:
                return get_object_or_404(self.get_queryset(), slug=lookup_value)
        except:
            return get_object_or_404(Category, id=None)

    @extend_schema(
        summary="Get category details",
        description="Retrieve category information including name, description, and count of products in this category. Use category ID or slug.",
        tags=['Categories']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update category",
        description="Update category name, description or image. All products in this category will reflect the changes. Requires admin authentication.",
        tags=['Categories']
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Partial update category",
        description="Update specific category fields like name or description. Requires admin authentication.",
        tags=['Categories']
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary="Delete category",
        description="Soft delete category (sets is_active=False). Cannot delete if category has active products. Requires admin authentication.",
        tags=['Categories']
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)