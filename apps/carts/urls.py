

# apps/carts/urls.py

"""
Cart URL Configuration - Consolidated

Consolidated URL patterns for cart operations.
All endpoints require user authentication.
"""

from django.urls import path
from .views import (
    CartView,
    CartItemView,
)

app_name = 'carts'

urlpatterns = [
    # ========================================================================
    # CONSOLIDATED CART ENDPOINTS
    # ========================================================================
    
    # Main cart endpoint - handles GET, POST (add), DELETE (clear)
    path('', CartView.as_view(), name='cart-operations'),
    
    # Individual cart item endpoint - handles PUT, PATCH, DELETE
    path('<uuid:item_id>/', CartItemView.as_view(), name='cart-item-operations'),
]

# ========================================================================
# COMPLETE CART API ENDPOINTS STRUCTURE (CONSOLIDATED)
# ========================================================================
"""
Now your cart APIs will appear on the same lines like products:

ENDPOINT: /api/v1/carts/
├── GET     → View current user's cart
├── POST    → Add product to cart  
└── DELETE  → Clear entire cart

ENDPOINT: /api/v1/carts/{item_id}/
├── PUT     → Update item quantity
├── PATCH   → Partial update item quantity
└── DELETE  → Remove specific item from cart

EXAMPLE REQUESTS:

1. View cart:
   GET /api/v1/carts/

2. Add to cart:
   POST /api/v1/carts/
   {
     "product_id": "123e4567-e89b-12d3-a456-426614174000",
     "quantity": 2
   }

3. Clear cart:
   DELETE /api/v1/carts/

4. Update item quantity:
   PUT /api/v1/carts/456e7890-e89b-12d3-a456-426614174000/
   {
     "quantity": 5
   }

5. Remove item:
   DELETE /api/v1/carts/456e7890-e89b-12d3-a456-426614174000/

CLEAN API STRUCTURE - CONSOLIDATED LIKE PRODUCTS! 🎯
"""