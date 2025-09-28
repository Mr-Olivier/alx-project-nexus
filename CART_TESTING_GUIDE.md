# Cart API Setup & Testing Guide

## Overview

The Cart API allows users to manage shopping cart items before placing orders.

---

## API Endpoints

```
1. POST   /api/v1/carts/           → Add item to cart
2. GET    /api/v1/carts/           → View cart
3. PATCH  /api/v1/carts/{item_id}/ → Update item quantity
4. DELETE /api/v1/carts/{item_id}/ → Remove item from cart
5. DELETE /api/v1/carts/           → Clear entire cart
```

---

## Prerequisites

1. Server running: `http://localhost:8000`
2. Authentication token from login API
3. Products created in database
4. Swagger UI: `http://localhost:8000/api/schema/swagger-ui/`

---

## Complete Testing Flow

### STEP 1: Create Products First

```json
POST /api/v1/products/

{
  "name": "Gaming Laptop",
  "description": "High performance laptop",
  "price": 1299.99,
  "category": "Electronics",
  "stock_quantity": 50
}
```

**Response:**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Gaming Laptop",
  "price": "1299.99",
  "stock_quantity": 50
}
```

**Copy the `product_id` for next step!**

---

### STEP 2: Add Item to Cart

```json
POST /api/v1/carts/

{
  "product_id": "550e8400-e29b-41d4-a716-446655440000",
  "quantity": 2
}
```

**Response:**

```json
{
  "message": "Product added to cart successfully",
  "cart_item": {
    "id": "cart-item-uuid",
    "product_id": "550e8400-e29b-41d4-a716-446655440000",
    "product_name": "Gaming Laptop",
    "product_slug": "gaming-laptop",
    "product_image": "http://localhost:8000/media/products/laptop.jpg",
    "quantity": 2,
    "unit_price": "1299.99",
    "subtotal": "2599.98",
    "is_available": true,
    "stock_available": 50
  }
}
```

---

### STEP 3: Add More Items

```json
POST /api/v1/carts/

{
  "product_id": "another-product-uuid",
  "quantity": 1
}
```

---

### STEP 4: View Cart

```
GET /api/v1/carts/
```

**Response:**

```json
{
  "id": "cart-uuid",
  "items": [
    {
      "id": "item-uuid-1",
      "product_id": "550e8400-e29b-41d4-a716-446655440000",
      "product_name": "Gaming Laptop",
      "product_slug": "gaming-laptop",
      "product_image": "http://localhost:8000/media/products/laptop.jpg",
      "quantity": 2,
      "unit_price": "1299.99",
      "subtotal": "2599.98",
      "is_available": true,
      "stock_available": 50
    },
    {
      "id": "item-uuid-2",
      "product_id": "another-product-uuid",
      "product_name": "Wireless Mouse",
      "quantity": 1,
      "unit_price": "49.99",
      "subtotal": "49.99",
      "is_available": true,
      "stock_available": 100
    }
  ],
  "total_items": 3,
  "total_price": "2649.97",
  "total_compare_price": "2899.97",
  "total_savings": "250.00"
}
```

---

### STEP 5: Update Item Quantity

```json
PATCH /api/v1/carts/item-uuid-1/

{
  "quantity": 3
}
```

**Response:**

```json
{
  "message": "Cart item updated successfully",
  "cart_item": {
    "id": "item-uuid-1",
    "product_name": "Gaming Laptop",
    "quantity": 3,
    "unit_price": "1299.99",
    "subtotal": "3899.97"
  }
}
```

---

### STEP 6: Remove Single Item

```
DELETE /api/v1/carts/item-uuid-1/
```

**Response:**

```json
{
  "message": "Item removed from cart successfully"
}
```

---

### STEP 7: Clear Entire Cart

```
DELETE /api/v1/carts/
```

**Response:**

```json
{
  "message": "Cart cleared successfully"
}
```

---

## Testing in Swagger UI

### 1. Authorize

- Click "Authorize" button
- Enter: `Bearer your-access-token`
- Click "Authorize"

### 2. Add Item to Cart

- Navigate to `POST /api/v1/carts/`
- Click "Try it out"
- Enter request body:
  ```json
  {
    "product_id": "your-product-uuid",
    "quantity": 2
  }
  ```
- Click "Execute"

### 3. View Cart

- Navigate to `GET /api/v1/carts/`
- Click "Try it out"
- Click "Execute"
- See your cart items

### 4. Update Quantity

- Navigate to `PATCH /api/v1/carts/{item_id}/`
- Click "Try it out"
- Enter cart item ID
- Enter new quantity
- Click "Execute"

### 5. Remove Item

- Navigate to `DELETE /api/v1/carts/{item_id}/`
- Click "Try it out"
- Enter cart item ID
- Click "Execute"

---

## Testing with cURL

### Add Item to Cart:

```bash
curl -X POST http://localhost:8000/api/v1/carts/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": "550e8400-e29b-41d4-a716-446655440000",
    "quantity": 2
  }'
```

### View Cart:

```bash
curl -X GET http://localhost:8000/api/v1/carts/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Update Item Quantity:

```bash
curl -X PATCH http://localhost:8000/api/v1/carts/ITEM_ID/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"quantity": 5}'
```

### Remove Item:

```bash
curl -X DELETE http://localhost:8000/api/v1/carts/ITEM_ID/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Clear Cart:

```bash
curl -X DELETE http://localhost:8000/api/v1/carts/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Validation Rules

### Add to Cart Validation:

- Product must exist and be active
- Quantity must be between 1 and 999
- Sufficient stock must be available
- Duplicate products update existing cart item

### Update Quantity Validation:

- Quantity must be between 1 and 999
- Stock availability is checked
- Cannot exceed available stock

---

## Common Errors & Solutions

### Error: "Product not found or is not active"

**Solution:**

- Verify product ID is correct
- Ensure product `is_active=True`
- Check product exists in database

### Error: "Only X items available in stock"

**Solution:**

- Reduce quantity to available stock
- Check product stock quantity

### Error: "Quantity must be at least 1"

**Solution:**

- Use quantity ≥ 1
- To remove item, use DELETE endpoint instead

### Error: "Quantity cannot exceed 999"

**Solution:**

- Maximum quantity per item is 999
- Split into multiple orders if needed

### Error: "Cart is empty"

**Solution:**

- Add items to cart first
- Verify you have items in cart with GET request

### Error: "Cart item not found"

**Solution:**

- Verify cart item ID is correct
- Item may have been removed already
- Get cart items with GET /api/v1/carts/

---

## Testing Scenarios

### Scenario 1: Add Multiple Products

1. Add product A (quantity: 2)
2. Add product B (quantity: 1)
3. Add product C (quantity: 3)
4. View cart (should show 6 total items)

### Scenario 2: Update Quantities

1. Add product (quantity: 2)
2. Update to quantity: 5
3. View cart (should show 5 items)

### Scenario 3: Stock Validation

1. Product has stock: 10
2. Try adding quantity: 15
3. Should fail with "Only 10 items available"

### Scenario 4: Duplicate Products

1. Add product A (quantity: 2)
2. Add same product A (quantity: 3)
3. Cart should have 1 item with quantity: 5 (merged)

### Scenario 5: Remove Items

1. Add 3 different products
2. Remove 1 product
3. View cart (should show 2 products)

### Scenario 6: Clear Cart

1. Add multiple products
2. Clear cart
3. View cart (should be empty)

---

## Cart Features

### Automatic Calculations:

- **Subtotal:** unit_price × quantity
- **Total Price:** Sum of all subtotals
- **Total Savings:** Compare price - actual price
- **Total Items:** Sum of all quantities

### Stock Management:

- Real-time stock availability check
- `is_available` flag for each item
- `stock_available` shows current stock

### Product Information:

- Product name, image, SKU included
- Links to product detail page
- Price information preserved

---

## Integration with Orders

After cart is ready:

1. **View cart** → Verify items and total
2. **Create order** → `POST /api/v1/orders/`
3. **Cart auto-clears** → After successful order
4. **Stock reduced** → Product inventory updated

---

## Quick Test Script

```bash
# 1. Add item to cart
curl -X POST http://localhost:8000/api/v1/carts/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "PRODUCT_ID", "quantity": 2}'

# 2. View cart
curl -X GET http://localhost:8000/api/v1/carts/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# 3. Update quantity (replace ITEM_ID)
curl -X PATCH http://localhost:8000/api/v1/carts/ITEM_ID/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"quantity": 5}'

# 4. Remove item
curl -X DELETE http://localhost:8000/api/v1/carts/ITEM_ID/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Verification Checklist

```
□ Can add products to cart
□ Can view cart with all items
□ Cart shows correct totals
□ Can update item quantities
□ Stock validation works
□ Can remove single items
□ Can clear entire cart
□ Cart auto-clears after order
□ Duplicate products merge correctly
□ Out-of-stock products blocked
```

---

## Complete Shopping Flow

```
1. Browse Products     → GET /api/v1/products/
2. Add to Cart         → POST /api/v1/carts/
3. View Cart           → GET /api/v1/carts/
4. Update Quantities   → PATCH /api/v1/carts/{item_id}/
5. Remove Items        → DELETE /api/v1/carts/{item_id}/
6. Create Order        → POST /api/v1/orders/
7. Cart Auto-Cleared   → (automatic)
```

**Your cart system is ready to test!**
