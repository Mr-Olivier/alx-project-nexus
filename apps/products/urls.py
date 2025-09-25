# # # apps/products/urls.py

# # """
# # Products URL Configuration

# # Defines essential URL patterns for product endpoints.
# # Clean and consistent URL structure.
# # """

# # from django.urls import path
# # from .views import (
# #     ProductListView,
# #     ProductDetailView,
# #     ProductCreateView,
# # )

# # app_name = 'products'

# # urlpatterns = [
# #     # ========================================================================
# #     # PRODUCT ENDPOINTS
# #     # ========================================================================
    
# #     # Product operations - all on same level
# #     # Note: 'products/' prefix is already in main urls.py, so we don't repeat it here
# #     path('', ProductListView.as_view(), name='product-list'),                    # /api/v1/products/
# #     path('create/', ProductCreateView.as_view(), name='product-create'),         # /api/v1/products/create/
# #     path('<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),    # /api/v1/products/{slug}/
# # ]




# # apps/products/urls.py

# """
# Products URL Configuration

# RESTful URL patterns with all CRUD operations on the same resource path.
# All operations are now grouped under the main products endpoint.
# """

# from django.urls import path
# from .views import (
#     ProductListCreateView,
#     ProductDetailUpdateDeleteView,
# )

# app_name = 'products'

# urlpatterns = [
#     # ========================================================================
#     # CONSOLIDATED PRODUCT ENDPOINTS - ALL ON SAME PATH
#     # ========================================================================
    
#     # Main products endpoint - handles LIST and CREATE
#     path('', ProductListCreateView.as_view(), name='product-list-create'),
    
#     # Individual product endpoint - handles DETAIL, UPDATE, DELETE
#     path('<str:pk>/', ProductDetailUpdateDeleteView.as_view(), name='product-detail-update-delete'),
# ]

# # ========================================================================
# # COMPLETE API ENDPOINTS STRUCTURE (ALL 5 OPERATIONS)
# # ========================================================================
# """
# Now you'll see ALL 5 essential e-commerce APIs in your documentation:

# ENDPOINT: /api/v1/products/
# ├── GET     → List all products with filtering/search/pagination
# └── POST    → Create new product (Admin only)

# ENDPOINT: /api/v1/products/{id}/
# ├── GET     → Get product details  
# ├── PUT     → Full update product (Admin only)
# ├── PATCH   → Partial update product (Admin only)
# └── DELETE  → Delete product (Admin only)

# FILTERING OPTIONS for GET /api/v1/products/:
# - ?category=shoes                             → Filter by category slug
# - ?category=uuid-here                         → Filter by category ID  
# - ?min_price=100&max_price=500               → Price range filter
# - ?is_featured=true                          → Featured products only
# - ?in_stock=true                             → In-stock products only
# - ?on_sale=true                              → Products on sale only
# - ?search=laptop                             → Search in name/description/SKU
# - ?ordering=-price                           → Sort by price (descending)
# - ?ordering=name                             → Sort by name (ascending)

# EXAMPLE REQUESTS:

# 1. List all products:
#    GET /api/v1/products/

# 2. Search for laptops under $1000:
#    GET /api/v1/products/?search=laptop&max_price=1000

# 3. Get product by ID:
#    GET /api/v1/products/123e4567-e89b-12d3-a456-426614174000/

# 4. Get product by slug:
#    GET /api/v1/products/awesome-laptop/

# 5. Create new product (Admin only):
#    POST /api/v1/products/
#    {
#      "name": "New Product",
#      "description": "Product description", 
#      "price": "99.99",
#      "category_id": "uuid-here",
#      "stock_quantity": 100
#    }

# 6. Update product (Admin only):
#    PATCH /api/v1/products/awesome-laptop/
#    {
#      "price": "89.99",
#      "stock_quantity": 50
#    }

# 7. Delete product (Admin only):
#    DELETE /api/v1/products/awesome-laptop/

# """




# apps/products/urls.py

"""
Products & Categories URL Configuration

Complete URL patterns for products and categories CRUD operations.
"""

from django.urls import path
from .views import (
    # Product views
    ProductListCreateView,
    ProductDetailUpdateDeleteView,
    # Category views
    CategoryListCreateView,
    CategoryDetailUpdateDeleteView,
)

app_name = 'products'

urlpatterns = [
    # ========================================================================
    # PRODUCT ENDPOINTS
    # ========================================================================
    
    # Product List & Create
    path('', ProductListCreateView.as_view(), name='product-list-create'),
    
    # Individual product endpoint
    path('<str:pk>/', ProductDetailUpdateDeleteView.as_view(), name='product-detail-update-delete'),
    
    # ========================================================================
    # CATEGORY ENDPOINTS
    # ========================================================================
    
    # Category List & Create
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    
    # Individual category endpoint
    path('categories/<str:pk>/', CategoryDetailUpdateDeleteView.as_view(), name='category-detail-update-delete'),
]

# ========================================================================
# COMPLETE API ENDPOINTS STRUCTURE
# ========================================================================
"""
PRODUCTS ENDPOINTS:
- GET    /api/v1/products/           → List all products with filtering
- POST   /api/v1/products/           → Create new product (Admin only)
- GET    /api/v1/products/{id}/      → Get product details  
- PUT    /api/v1/products/{id}/      → Full update product (Admin only)
- PATCH  /api/v1/products/{id}/      → Partial update product (Admin only)
- DELETE /api/v1/products/{id}/      → Delete product (Admin only)

CATEGORIES ENDPOINTS:
- GET    /api/v1/products/categories/           → List all categories
- POST   /api/v1/products/categories/           → Create new category (Admin only)
- GET    /api/v1/products/categories/{id}/      → Get category details
- PUT    /api/v1/products/categories/{id}/      → Full update category (Admin only)
- PATCH  /api/v1/products/categories/{id}/      → Partial update category (Admin only)
- DELETE /api/v1/products/categories/{id}/      → Delete category (Admin only)

EXAMPLE REQUESTS:

Categories:
1. List categories:
   GET /api/v1/products/categories/

2. Create category (Admin):
   POST /api/v1/products/categories/
   {"name": "Electronics", "description": "Electronic devices"}

3. Get category details:
   GET /api/v1/products/categories/electronics/

Products with Categories:
4. Filter products by category:
   GET /api/v1/products/?category=electronics

5. Create product with category:
   POST /api/v1/products/
   {"name": "Laptop", "category_id": "uuid-here", ...}
"""