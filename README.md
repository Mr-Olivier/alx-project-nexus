# 🛒 ALX Project Nexus – E-Commerce API

A **Django-based eCommerce backend** powered by PostgreSQL, Django REST Framework, Stripe (test mode), and Mailtrap OTP.  
Includes **API documentation**, testing guides, and a simple setup process for quick onboarding.

---

## 📦 Features

- 🔑 **Authentication & OTP** (via Mailtrap)
- 🛍️ **Products**
- 🛒 **Carts & Orders**
- 💳 **Stripe Payments** (test mode)
- 📖 **Swagger API Documentation**

---

## 🚀 Quick Start

### 1️⃣ Clone the Project

```bash
git clone <your-repo-url>
cd alx-project-nexus
```

2️⃣ Configure Environment Variables

Copy the example file and update with your values:
cp .env.example .env

Fill in:

Database credentials

Mailtrap API keys

Stripe test keys

💡 Use test values if you’re just running locally.

⚙️ Setup & Run

See the full setup guide in TEST_TO_RUN.md
.
It covers:

Creating a virtual environment

Installing dependencies

Running migrations

Starting the development server

🧪 Testing APIs

We’ve included step-by-step guides for testing each feature:

Feature Guide
🔑 Auth & OTP AUTH_TESTING.md

🛍️ Products PRODUCT_TESTING.md

🛒 Carts CART_TESTING_GUIDE.md

📦 Orders ORDER_TESTING.md

💳 Payments PAYMENT_TESTING_GUIDE.md
📄 API Documentation

After starting the server, explore APIs using Swagger UI:

👉 http://127.0.0.1:8000/api/schema/swagger-ui/

🛠️ Tech Stack

Backend: Django + Django REST Framework

Database: PostgreSQL

Email: Mailtrap (OTP support)

Payments: Stripe (test mode)

Docs: Swagger UI

📌 Notes

Always activate your virtual environment before running the project.

Use .env.example as a reference for required environment variables.

Stick with test keys for Stripe and Mailtrap until production.
