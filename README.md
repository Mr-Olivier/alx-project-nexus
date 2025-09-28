# 🛒 ALX Project Nexus – E-Commerce API

This is a **Django-based eCommerce backend** with PostgreSQL, REST API, Stripe payments, and Mailtrap OTP support.  
This project includes **API documentation**, testing guides, and an easy-to-follow setup process.

---

## 📦 Features

- ✅ **Authentication & OTP** (Mailtrap)
- ✅ **Products & Categories**
- ✅ **Carts & Orders**
- ✅ **Stripe Payments (Test Mode)**
- ✅ **Swagger API Documentation**

---

## 🚀 Quick Start Guide

### 1️⃣ Clone the Project

```bash
git clone <repository-url>
cd alx-project-nexus
2️⃣ Create .env File
Copy .env.example to .env and fill in your values:

bash
Copy code
cp .env.example .env
Add your database credentials, Mailtrap keys, and Stripe test keys

Use test values if you just want to run it locally

📖 Setup & Testing Guide
To set up and run the project, follow the full guide here:
📄 TEST_TO_RUN.md

It explains:

Creating virtual environment

Installing dependencies

Running migrations

Starting the development server

🧪 Testing APIs
We included step-by-step guides for testing APIs.
Follow them to check each feature:

Feature	Guide
🔑 Auth & OTP	AUTH_TESTING.md
🛍️ Products	PRODUCT_TESTING.md
🛒 Carts	CART_TESTING_GUIDE.md
📦 Orders	ORDER_TESTING.md
💳 Payments	PAYMENT_TESTING_GUIDE.md

🗄️ Swagger Documentation
Once the server is running, visit:

Swagger Docs: http://127.0.0.1:8000/api/schema/swagger-ui/

🛠️ Tech Stack
Backend: Django + Django REST Framework

Database: PostgreSQL

Email: Mailtrap (for OTP)

Payments: Stripe (test mode)

Docs: Swagger UI

📌 Notes
Always activate your virtual environment before running the project

Use .env.example as a reference for required environment variables

Use test keys for Stripe and Mailtrap until you go live

🤝 Contributing
Pull requests and issues are welcome!

📜 License
Licensed under MIT – you are free to use, modify, and share.

yaml
Copy code

---

✅ **Why this is good:**
- Short & clean (doesn’t repeat `TEST_TO_RUN.md`)
- Clearly points to `.env.example` and tells them to copy it
- Links to all your test guides so they know where to look
- Mentions Swagger docs link for easy API exploration

---

Would you like me to also write you a **`.env.example` file** with placeholders for PostgreSQL, Mailtrap, and Stripe (so your README reference works out of the box)
```
