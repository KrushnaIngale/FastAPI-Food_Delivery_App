# 🍔 FastAPI Food Delivery Backend

A complete backend system built using **FastAPI** as part of internship training.  
This project simulates a real-world food delivery application with menu management, cart system, order processing, and advanced API features.

---

## 🚀 Features

### 📌 Core APIs
- Get all menu items
- Get item by ID
- Menu summary (available/unavailable items)

### 📌 Data Validation (Pydantic)
- Request validation for orders and checkout
- Field constraints (min/max values)

### 📌 CRUD Operations
- Add new menu item
- Update item price and availability
- Delete menu item

### 📌 Cart & Order Workflow
- Add items to cart
- Update quantity (no duplicates)
- Remove items from cart
- Checkout system → creates orders
- Order tracking

### 📌 Advanced APIs
- 🔍 Search (name + category)
- 🔽 Sorting (price, name, category)
- 📄 Pagination
- 🧠 Combined browse (filter + sort + pagination)

---

## 🛠 Tech Stack

- Python
- FastAPI
- Pydantic
- Uvicorn

---

## ▶️ How to Run

```bash
pip install -r requirements.txt
uvicorn main:app --reload