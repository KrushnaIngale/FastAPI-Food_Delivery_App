# 🍔 QuickBite+ Smart Food Ordering System (FastAPI)

## 📌 Project Overview

QuickBite+ is a FastAPI-based backend system that simulates a real-world food ordering workflow — from browsing menu items to placing and processing orders.

The focus of this project is not just building endpoints, but designing a **structured backend system** with validation, workflow management, and efficient data handling.

---

## 🚀 Key Features

### 🔹 Core APIs
- Home route (`/`)
- Get full menu (`/menu`)
- Get item by ID (`/menu/{item_id}`)
- Menu insights (`/menu/summary`)

---

### 🔹 Data Validation (Pydantic)
- Strong request validation using Pydantic models
- Field constraints:
  - Quantity limits
  - Valid IDs
  - Minimum address length
- Automatic error responses for invalid inputs

---

### 🔹 CRUD Operations
- Add new menu items
- Update price and availability
- Delete menu items
- Retrieve records

✔ Proper use of HTTP status codes: `201`, `400`, `404`

---

### 🔹 Cart & Order Workflow (Core Logic)

A complete multi-step flow:

Cart → Add Items → Update Quantity → Remove Items → Checkout → Orders

✔ Prevents duplicate cart entries  
✔ Validates item availability  
✔ Converts cart into confirmed orders  

---

### 🔹 Advanced API Features

#### 🔍 Search
`/menu/search?keyword=pizza`  
Search across name and category (case-insensitive)

#### 🎯 Filter
`/menu/filter?category=Pizza&max_price=300&is_available=true`

#### 🔃 Sort
`/menu/sort?sort_by=price&order=desc`

#### 📄 Pagination
`/menu/page?page=1&limit=3`

#### ⚡ Smart Browse (Combined API)
`/menu/browse`

Supports:
- keyword
- sort_by
- order
- page
- limit

✔ Processing order:
**Filter → Sort → Pagination**

---

## 🧠 Design Highlights

- Clean separation of logic using helper functions:
  - `find_menu_item()`
  - `calculate_bill()`
  - `filter_menu_logic()`
- Case-insensitive operations for better usability
- Dynamic filtering using `Query()` and `is not None`
- Route structuring to avoid conflicts (static before dynamic)
- Realistic backend workflow implementation

---

## 🛠 Tech Stack

- Python
- FastAPI
- Pydantic
- Uvicorn

---

## ▶️ Running the Project

### Install dependencies
```bash
pip install -r requirements.txt

### Start server
```bash
uvicorn main:app --reload

### Access API Docs
```bash
http://127.0.0.1:8000/docs

###📸 Screenshots

- All API responses (Q1–Q20) are documented in the screenshots/ folder.

### 📂 Project Structure
```bash
main.py
requirements.txt
README.md
screenshots/