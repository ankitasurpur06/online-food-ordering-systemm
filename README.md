# 🍽️ QuickBite — Django Web Application

A fully integrated Django web application for gourmet food delivery, with a Single-Page Application (SPA) frontend backed by a Python/Django REST API.

---

## 📁 Project Structure

```
quickbite/
├── manage.py
├── requirements.txt
├── db.sqlite3                  ← auto-created on first run
├── quickbite/                  ← Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── core/                       ← Main Django app
    ├── models.py               ← Database models
    ├── views.py                ← API views
    ├── urls.py                 ← URL routing
    ├── admin.py                ← Django admin config
    ├── templates/
    │   └── core/
    │       └── index.html      ← SPA template (Django-integrated)
    └── management/
        └── commands/
            └── seed_data.py    ← Database seeder
```

---

## 🚀 Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Seed the Database
```bash
python manage.py seed_data
```

### 4. Start the Server
```bash
python manage.py runserver
```

### 5. Open in Browser
Visit: **http://127.0.0.1:8000/**

---

## 👤 Demo Accounts

| Role  | Email                    | Password  |
|-------|--------------------------|-----------|
| Admin | admin@quickbite.com      | admin123  |
| User  | user@quickbite.com       | user123   |

---

## 🔗 API Endpoints

| Method | URL                          | Description            |
|--------|------------------------------|------------------------|
| POST   | `/api/auth/login/`           | User login             |
| POST   | `/api/auth/register/`        | User registration      |
| POST   | `/api/auth/logout/`          | User logout            |
| GET    | `/api/auth/me/`              | Current user + stats   |
| GET    | `/api/restaurants/`          | List + filter rests    |
| GET    | `/api/restaurants/<id>/`     | Restaurant + menu      |
| POST   | `/api/orders/place/`         | Place an order         |
| GET    | `/api/orders/history/`       | User's order history   |
| GET    | `/api/favourites/`           | User's favourites      |
| POST   | `/api/favourites/toggle/`    | Toggle favourite       |
| POST   | `/api/address/update/`       | Update delivery addr   |
| POST   | `/api/promo/apply/`          | Apply promo code       |
| GET    | `/api/search/?q=`            | Live search            |
| GET    | `/api/admin/stats/`          | Admin KPIs + data      |

---

## 🗄️ Database Models

- **UserProfile** — extended user info
- **Address** — saved delivery addresses
- **Cuisine** — cuisine categories
- **Restaurant** — restaurant listings
- **MenuItem** — menu items per restaurant
- **Order** — placed orders with status
- **OrderItem** — individual items in order
- **PromoCode** — discount codes
- **Favourite** — user favourite restaurants
- **Review** — user reviews

---

## ⚙️ Django Admin

Visit: **http://127.0.0.1:8000/admin/**
Login with: `admin@quickbite.com / admin123`

---

## 🛠️ Tech Stack

- **Backend**: Python 3.x + Django 4.2
- **Database**: SQLite (dev) — swap to PostgreSQL for production
- **Frontend**: Vanilla JS SPA integrated into Django templates
- **API**: Django JSON views (REST-style, no DRF required)
- **Auth**: Django's built-in session authentication
- **Fonts**: Google Fonts (Playfair Display + DM Sans)
- **Images**: Unsplash CDN
