# Payment API Setup & Testing Guide (Without Webhooks)

## Quick Setup Guide for New Users

### Step 1: Get Stripe Test API Keys

1. **Sign up at Stripe:** https://stripe.com (Free account)
2. **Go to Dashboard:** https://dashboard.stripe.com/test/apikeys
3. **Copy your test keys:**
   - **Secret key** (starts with `sk_test_...`)
   - **Publishable key** (starts with `pk_test_...`)

### Step 2: Configure Environment Variables

Create a `.env` file in the project root:

```bash
# .env

# Stripe Test Keys
STRIPE_SECRET_KEY=sk_test_your_secret_key_here
STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key_here
STRIPE_WEBHOOK_SECRET=
```

**Note:** Leave `STRIPE_WEBHOOK_SECRET` empty - webhooks are not required for testing.

### Step 3: Install Dependencies

```bash
pip install stripe python-decouple
```

### Step 4: Run Migrations

```bash
python manage.py makemigrations payments
python manage.py migrate payments
python manage.py runserver
```

---

## Testing Payment APIs

### Prerequisites

1. Server running: `http://localhost:8000`
2. Authentication token from login API
3. Swagger UI: `http://localhost:8000/api/schema/swagger-ui/`

---

## Complete Testing Flow

### STEP 1: Create Products & Add to Cart

**1.1 Create a product:**

```json
POST /api/v1/products/

{
  "name": "Laptop",
  "description": "Gaming laptop",
  "price": 1200.00,
  "category": "Electronics",
  "stock_quantity": 10
}
```

**1.2 Add product to cart:**

```json
POST /api/v1/carts/

{
  "product_id": "product-uuid-from-step-1",
  "quantity": 2
}
```

---

### STEP 2: Create Order

```json
POST /api/v1/orders/

{
  "shipping_address": "123 Main St",
  "shipping_city": "Kigali",
  "shipping_country": "Rwanda"
}
```

**Response:**

```json
{
  "message": "Order placed successfully",
  "order": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "pending",
    "total_amount": "2400.00"
  }
}
```

**Copy the `order_id` for next step!**

---

### STEP 3: Create Payment Checkout Session

```json
POST /api/v1/payments/create-checkout-session/

{
  "order_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response:**

```json
{
  "checkout_url": "https://checkout.stripe.com/c/pay/cs_test_a1...",
  "session_id": "cs_test_a1b2c3d4e5f6g7h8",
  "order_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Copy both `checkout_url` and `session_id`!**

---

### STEP 4: Complete Payment

1. **Copy the `checkout_url`** from response
2. **Open in web browser**
3. **Enter Stripe test card details:**
   - **Card Number:** `4242 4242 4242 4242`
   - **Expiry Date:** `12/34` (any future date)
   - **CVC:** `123` (any 3 digits)
   - **ZIP:** `12345` (any 5 digits)
4. **Click "Pay"**
5. You'll see payment success page

---

### STEP 5: Check Payment Status

```
GET /api/v1/payments/session-status/cs_test_a1b2c3d4e5f6g7h8/
```

Replace `cs_test_a1b2c3d4e5f6g7h8` with your actual `session_id`.

**Response (Payment Successful):**

```json
{
  "order_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "paid",
  "amount": "2400.00",
  "payment_date": "2025-09-26T22:30:00Z"
}
```

**Response (Payment Pending):**

```json
{
  "order_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "amount": "2400.00",
  "payment_date": null
}
```

---

### STEP 6: View Payment Details

```
GET /api/v1/payments/order/550e8400-e29b-41d4-a716-446655440000/
```

**Response:**

```json
{
  "id": "payment-uuid",
  "order_id": "550e8400-e29b-41d4-a716-446655440000",
  "order_status": "processing",
  "order_total": "2400.00",
  "amount": "2400.00",
  "currency": "usd",
  "status": "paid",
  "status_display": "Paid",
  "payment_method": "card",
  "transaction_id": "pi_3Nq...",
  "payment_date": "2025-09-26T22:30:00Z"
}
```

---

## Stripe Test Cards

### Successful Payments:

- **4242 4242 4242 4242** - Visa (Always succeeds)
- **5555 5555 5555 4444** - Mastercard (Always succeeds)
- **3782 822463 10005** - American Express (Always succeeds)

### Failed Payments (For Testing Errors):

- **4000 0000 0000 0002** - Card declined
- **4000 0000 0000 9995** - Insufficient funds
- **4000 0000 0000 0069** - Expired card

### Card Details (Use for All Test Cards):

- **Expiry:** Any future date (e.g., `12/34`)
- **CVC:** Any 3 digits (e.g., `123`)
- **ZIP:** Any 5 digits (e.g., `12345`)

---

## API Endpoints Summary

```
1. POST   /api/v1/payments/create-checkout-session/
   → Create Stripe checkout session

2. GET    /api/v1/payments/session-status/{session_id}/
   → Check payment status

3. GET    /api/v1/payments/order/{order_id}/
   → Get payment details for order
```

---

## Testing in Swagger UI

### 1. Authorize

- Click "Authorize" button
- Enter: `Bearer your-access-token`
- Click "Authorize"

### 2. Create Checkout Session

- Navigate to `POST /api/v1/payments/create-checkout-session/`
- Click "Try it out"
- Enter your `order_id`
- Click "Execute"
- **Copy the `checkout_url`**

### 3. Complete Payment

- Open `checkout_url` in browser
- Enter test card: `4242 4242 4242 4242`
- Complete payment

### 4. Check Payment Status

- Navigate to `GET /api/v1/payments/session-status/{session_id}/`
- Click "Try it out"
- Enter your `session_id`
- Click "Execute"
- Should show `"status": "paid"`

---

## Testing with cURL

### Create Checkout Session:

```bash
curl -X POST http://localhost:8000/api/v1/payments/create-checkout-session/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"order_id": "YOUR_ORDER_ID"}'
```

### Check Payment Status:

```bash
curl -X GET http://localhost:8000/api/v1/payments/session-status/YOUR_SESSION_ID/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Get Payment Details:

```bash
curl -X GET http://localhost:8000/api/v1/payments/order/YOUR_ORDER_ID/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Common Errors & Solutions

### Error: "STRIPE_SECRET_KEY not configured"

**Solution:**

- Add `STRIPE_SECRET_KEY` to `.env` file
- Make sure it starts with `sk_test_`

### Error: "Order not found or does not belong to you"

**Solution:**

- Create an order first using `/api/v1/orders/`
- Use the correct `order_id` from your own user's orders

### Error: "Order is already paid"

**Solution:**

- This order was already paid
- Create a new order to test again

### Error: "Cannot pay for order with status: Processing"

**Solution:**

- Only orders with status "pending" can be paid
- Create a new order

### Error: Invalid API Key

**Solution:**

- Check your Stripe secret key is correct
- Make sure you're using test key (starts with `sk_test_`)

### Error: "No such checkout session"

**Solution:**

- Use the correct `session_id` from create-checkout response
- Session IDs start with `cs_test_`

---

## Verification Checklist

After setup, verify:

```
□ Stripe test keys added to .env
□ Dependencies installed (stripe, python-decouple)
□ Migrations applied
□ Server running successfully
□ Can create products
□ Can add to cart
□ Can create order
□ Can create checkout session
□ Can complete payment with test card
□ Can check payment status
□ Can view payment details
□ Order status changes to "processing" after payment
```

---

## Notes About Webhooks

**Webhooks are NOT required for this setup.**

- Webhooks provide automatic payment updates from Stripe
- For testing/demo purposes, manually checking status works perfectly
- The flow works: Create checkout → Pay → Check status manually

**If you see webhook-related code:**

- It's optional and can be ignored
- The webhook endpoint is commented out in URLs
- Leave `STRIPE_WEBHOOK_SECRET` empty in `.env`

---

## Testing Different Scenarios

### Scenario 1: Successful Payment Flow

1. Create order → Create checkout → Pay with `4242 4242 4242 4242` → Check status (paid)

### Scenario 2: Declined Payment

1. Create order → Create checkout → Pay with `4000 0000 0000 0002` → Payment fails

### Scenario 3: Multiple Orders

1. Create multiple orders
2. Pay for each separately
3. View payment history for each order

### Scenario 4: Already Paid Order

1. Try creating checkout for already paid order
2. Should receive error: "Order is already paid"

---

## Quick Test Script

```bash
# 1. Create order (copy order_id from response)
curl -X POST http://localhost:8000/api/v1/orders/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"shipping_city": "Kigali"}'

# 2. Create checkout (replace ORDER_ID)
curl -X POST http://localhost:8000/api/v1/payments/create-checkout-session/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"order_id": "ORDER_ID"}'

# 3. Open checkout_url in browser and pay with 4242 4242 4242 4242

# 4. Check status (replace SESSION_ID)
curl -X GET http://localhost:8000/api/v1/payments/session-status/SESSION_ID/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## View Payments in Stripe Dashboard

1. Go to: https://dashboard.stripe.com/test/payments
2. See all test payments
3. Click on any payment to see details
4. Verify amounts match your orders

---

## Support & Troubleshooting

If you encounter issues:

1. **Check Stripe Dashboard:** https://dashboard.stripe.com/test/payments
2. **Verify test mode:** Toggle should be ON (test mode)
3. **Check server logs:** Look for error messages
4. **Verify API keys:** Must start with `sk_test_` and `pk_test_`

---

## Complete E-commerce Flow

```
1. Browse Products    → GET /api/v1/products/
2. Add to Cart        → POST /api/v1/carts/
3. View Cart          → GET /api/v1/carts/
4. Create Order       → POST /api/v1/orders/
5. Create Checkout    → POST /api/v1/payments/create-checkout-session/
6. Complete Payment   → (Stripe Checkout Page)
7. Check Status       → GET /api/v1/payments/session-status/{id}/
8. View Payment       → GET /api/v1/payments/order/{order_id}/
9. Order Processing   → Order status = "processing"
```

**Your e-commerce payment system is ready to test!**
