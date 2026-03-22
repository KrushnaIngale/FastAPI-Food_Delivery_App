# IMPORTS
from fastapi import FastAPI, Query, Response
from pydantic import BaseModel, Field
from typing import Optional

# Q1 - App Initialization
app = FastAPI()

# Q2 - Menu Data
menu = [
    {"id": 1, "name": "Margherita Pizza", "price": 299, "category": "Pizza", "is_available": True},
    {"id": 2, "name": "Veg Burger", "price": 149, "category": "Burger", "is_available": True},
    {"id": 3, "name": "Coke", "price": 50, "category": "Drink", "is_available": True},
    {"id": 4, "name": "Brownie", "price": 120, "category": "Dessert", "is_available": False},
    {"id": 5, "name": "Pepperoni Pizza", "price": 399, "category": "Pizza", "is_available": True},
    {"id": 6, "name": "French Fries", "price": 99, "category": "Burger", "is_available": True}
]

# Orders + Cart
orders = []
order_counter = 1
cart = []

#-------------models----------
# Q6 - Order Request Model
class OrderRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    item_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0, le=20)
    delivery_address: str = Field(..., min_length=10)
    order_type: str = "delivery"


# Q11 - New Menu Item Model
class NewMenuItem(BaseModel):
    name: str = Field(..., min_length=2)
    price: int = Field(..., gt=0)
    category: str = Field(..., min_length=2)
    is_available: bool = True


# Q15 - Checkout Model
class CheckoutRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    delivery_address: str = Field(..., min_length=10)


# -----------helper functions-----------------
# Q7 - Helper Functions

def find_menu_item(item_id: int):
    for item in menu:
        if item["id"] == item_id:
            return item
    return None


def calculate_bill(price: int, quantity: int, order_type="delivery"):
    total = price * quantity
    if order_type.lower() == "delivery":
        total += 30
    return total


def filter_menu_logic(category=None, max_price=None, is_available=None):
    result = menu

    if category is not None:
        result = [i for i in result if i["category"].lower() == category.lower()]

    if max_price is not None:
        result = [i for i in result if i["price"] <= max_price]

    if is_available is not None:
        result = [i for i in result if i["is_available"] == is_available]

    return result


# ----------end-points----------
# BASIC ROUTES (Q1–Q5)
@app.get("/")
def home():
    return {"message": "Welcome to QuickBite Food Delivery"}

# Q4
@app.get("/orders")
def get_orders():
    return {"orders": orders,
            "total_orders": len(orders)}

@app.get("/menu")
def get_menu():
    return {"menu": menu, "total": len(menu)}


@app.get("/menu/summary")
def get_menu_summary():
    total = len(menu)
    available = len([i for i in menu if i["is_available"]])
    unavailable = total - available
    categories = list(set(i["category"] for i in menu))

    return {
        "total": total,
        "available": available,
        "unavailable": unavailable,
        "categories": categories
    }


# ADVANCED MENU APIs (Q10,16–20)
@app.get("/menu/filter")
def filter_menu(
    category: Optional[str] = Query(None),
    max_price: Optional[int] = Query(None),
    is_available: Optional[bool] = Query(None)
):
    result = filter_menu_logic(category, max_price, is_available)
    return {"items": result, "count": len(result)}


@app.get("/menu/search")
def search_menu(keyword: str = Query(...)):
    result = [
        item for item in menu
        if keyword.lower() in item["name"].lower()
        or keyword.lower() in item["category"].lower()
    ]

    if not result:
        return {"error": "No items found"}

    return {"results": result, "total_found": len(result)}


@app.get("/menu/sort")
def sort_menu(sort_by: str = "price", order: str = "asc"):
    if sort_by not in ["price", "name", "category"]:
        return {"error": "Invalid sort field"}

    if order not in ["asc", "desc"]:
        return {"error": "Invalid order"}
    
    reverse = True if order == "desc" else False

    sorted_menu = sorted(menu, key=lambda x: x[sort_by], reverse=reverse)

    return {
        "sorted_by": sort_by,
        "order": order, 
        "items": sorted_menu
    }


@app.get("/menu/page")
def paginate_menu(page: int = 1, limit: int = 3):
    start = (page - 1) * limit
    end = start + limit

    total = len(menu)
    total_pages = (total + limit - 1) // limit

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "items": menu[start:end]
    }


@app.get("/menu/browse")
def browse_menu(keyword: str = None, sort_by="price", order="asc", page=1, limit=4):
    result = menu

    if keyword:
        result = [
            i for i in result
            if keyword.lower() in i["name"].lower()
            or keyword.lower() in i["category"].lower()
        ]

    reverse = True if order == "desc" else False
    result = sorted(result, key=lambda x: x[sort_by], reverse=reverse)

    start = (page - 1) * limit
    end = start + limit

    total = len(result)
    total_pages = (total + limit - 1) // limit

    return {"total": total, "total_pages": total_pages, "page": page, "items": result[start:end]}


# CRUD (Q11–13)
@app.post("/menu")
def add_menu_item(item: NewMenuItem, response: Response):
    for m in menu:
        if m["name"].lower() == item.name.lower():
            response.status_code = 400
            return {"error": "Item already exists"}

    new_id = max([m["id"] for m in menu]) + 1

    new_item = item.dict()
    new_item["id"] = new_id

    menu.append(new_item)
    response.status_code = 201

    return new_item


@app.put("/menu/{item_id}")
def update_menu_item(item_id: int, price: int = Query(None), is_available: bool = Query(None), response: Response=Response):
    item = find_menu_item(item_id)

    if not item:
        response.status_code = 404
        return {"error": "Item not found"}

    if price is not None:
        item["price"] = price

    if is_available is not None:
        item["is_available"] = is_available

    return item


@app.delete("/menu/{item_id}")
def delete_menu_item(item_id: int, response: Response):
    item = find_menu_item(item_id)

    if not item:
        response.status_code = 404
        return {"error": "Item not found"}

    menu.remove(item)
    return {"message": f"{item['name']} deleted successfully"}

# DYNAMIC ROUTES
@app.get("/menu/{item_id}")
def get_menu_item(item_id: int):
    item = find_menu_item(item_id)
    if not item:
        return {"error": "Item not found"}
    return item


# Q 8
@app.post("/orders")
def place_order(order: OrderRequest):
    global order_counter
    item = find_menu_item(order.item_id)
    if not item:
        return {"error": "Item not found"}
    if not item['is_available']:
        return {"error": "Item is not available"}
    
    total_price = calculate_bill(item['price'], order.quantity, order.order_type)

    new_order={
        "order_id": order_counter,
        "customer_name": order.customer_name,
        "item": item["name"],
        "quantity": order.quantity,
        "total_price": total_price,
        "address": order.delivery_address
    }

    orders.append(new_order)
    order_counter+=1

    return new_order

# Q 19
@app.get("/orders/search")
def search_orders(customer_name: str):
    result = [
        o for o in orders
        if customer_name.lower() in o["customer_name"].lower()
    ]

    return {"orders": result}

@app.get("/orders/sort")
def sort_orders(order: str = "asc"):
    reverse = True if order == "desc" else False
    sorted_orders = sorted(orders, key=lambda x: x["total_price"], reverse=reverse)

    return {"orders": sorted_orders}

# Q 14
@app.post("/cart/add")
def add_to_cart(item_id: int, quantity: int = 1):
    item = find_menu_item(item_id)
    if not item:
        return {"error": "Item not found"}
    if not item["is_available"]:
        return {"error": f"{item['name']} is not available"}

    # check if already in cart
    for c in cart:
        if c["item_id"] == item_id:
            c["quantity"] += quantity
            return {"message": "Quantity updated", "cart": cart}

    cart.append({
        "item_id": item_id,
        "name": item["name"],
        "price": item["price"],
        "quantity": quantity
    })

    return {"message": "Item added to cart", "cart": cart}

@app.get("/cart")
def get_cart():
    total = sum(item["price"] * item["quantity"] for item in cart)
    return {
        "cart": cart,
        "grand_total": total
    }

# Q15
@app.delete("/cart/{item_id}")
def remove_from_cart(item_id: int):

    for item in cart:
        if item["item_id"] == item_id:
            cart.remove(item)
            return {"message": "Item removed from cart"}

    return {"error": "Item not in cart"}


@app.post("/cart/checkout")
def checkout(data: CheckoutRequest, response: Response):

    global order_counter

    if not cart:
        response.status_code = 400
        return {"error": "Cart is empty"}

    placed_orders = []
    grand_total = 0

    for item in cart:
        total_price = item["price"] * item["quantity"]
        grand_total += total_price

        order = {
            "order_id": order_counter,
            "customer_name": data.customer_name,
            "item": item["name"],
            "quantity": item["quantity"],
            "total_price": total_price,
            "address": data.delivery_address
        }

        orders.append(order)
        placed_orders.append(order)
        order_counter += 1

    cart.clear()
    response.status_code = 201

    return {
        "orders": placed_orders,
        "grand_total": grand_total
    }