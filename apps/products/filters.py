# apps/products/filters.py

"""
Product Filters

Advanced filtering capabilities for product listings.
Provides clean filter options for the API.
"""

import django_filters
from django.db import models
from .models import Product, Category


class ProductFilter(django_filters.FilterSet):
    """
    Advanced product filtering with multiple options
    """
    
    # Price range filters
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    
    # Category filters (supports both ID and slug)
    category = django_filters.CharFilter(method='filter_category')
    category_id = django_filters.UUIDFilter(field_name='category__id')
    category_slug = django_filters.CharFilter(field_name='category__slug')
    
    # Stock filters
    in_stock = django_filters.BooleanFilter(method='filter_in_stock')
    low_stock = django_filters.BooleanFilter(method='filter_low_stock')
    out_of_stock = django_filters.BooleanFilter(method='filter_out_of_stock')
    
    # Status filters
    is_featured = django_filters.BooleanFilter(field_name='is_featured')
    is_active = django_filters.BooleanFilter(field_name='is_active')
    on_sale = django_filters.BooleanFilter(method='filter_on_sale')
    
    # Stock quantity range
    min_stock = django_filters.NumberFilter(field_name='stock_quantity', lookup_expr='gte')
    max_stock = django_filters.NumberFilter(field_name='stock_quantity', lookup_expr='lte')
    
    # Date filters
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    updated_after = django_filters.DateTimeFilter(field_name='updated_at', lookup_expr='gte')
    updated_before = django_filters.DateTimeFilter(field_name='updated_at', lookup_expr='lte')
    
    # SKU filter
    sku = django_filters.CharFilter(field_name='sku', lookup_expr='icontains')
    
    class Meta:
        model = Product
        fields = {
            'name': ['exact', 'icontains'],
            'price': ['exact', 'gte', 'lte'],
            'stock_quantity': ['exact', 'gte', 'lte'],
            'is_featured': ['exact'],
            'is_active': ['exact'],
        }
    
    def filter_category(self, queryset, name, value):
        """Filter by category ID or slug"""
        if not value:
            return queryset
        
        # Check if it's a UUID (36 chars with dashes)
        if len(value) == 36 and '-' in value:
            try:
                return queryset.filter(category__id=value)
            except:
                pass
        
        # Otherwise treat as slug
        return queryset.filter(category__slug=value)
    
    def filter_in_stock(self, queryset, name, value):
        """Filter products that are in stock"""
        if value:
            return queryset.filter(stock_quantity__gt=0)
        return queryset.filter(stock_quantity=0)
    
    def filter_low_stock(self, queryset, name, value):
        """Filter products with low stock"""
        if value:
            return queryset.filter(
                stock_quantity__gt=0,
                stock_quantity__lte=models.F('low_stock_threshold')
            )
        return queryset.exclude(
            stock_quantity__gt=0,
            stock_quantity__lte=models.F('low_stock_threshold')
        )
    
    def filter_out_of_stock(self, queryset, name, value):
        """Filter products that are out of stock"""
        if value:
            return queryset.filter(stock_quantity=0)
        return queryset.filter(stock_quantity__gt=0)
    
    def filter_on_sale(self, queryset, name, value):
        """Filter products that are on sale (have compare_price > price)"""
        if value:
            return queryset.filter(
                compare_price__isnull=False,
                compare_price__gt=models.F('price')
            )
        return queryset.exclude(
            compare_price__isnull=False,
            compare_price__gt=models.F('price')
        )