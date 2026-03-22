# Q 1 - 5 day 1
from fastapi import FastAPI
# Q 6- 10 day 2
from pydantic import BaseModel, Field
# Q 10
from typing import Optional
from fastapi import Query
# Q 11
from fastapi import Response

# Q1
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to QuickBite Food Delivery"}

# Q2
menu = [
    {"id": 1, "name": "Margherita Pizza", "price": 299, "category": "Pizza", "is_available": True},
    {"id": 2, "name": "Veg Burger", "price": 149, "category": "Burger", "is_available": True},
    {"id": 3, "name": "Coke", "price": 50, "category": "Drink", "is_available": True},
    {"id": 4, "name": "Brownie", "price": 120, "category": "Dessert", "is_available": False},
    {"id": 5, "name": "Pepperoni Pizza", "price": 399, "category": "Pizza", "is_available": True},
    {"id": 6, "name": "French Fries", "price": 99, "category": "Burger", "is_available": True}
]

orders = []
order_counter = 1
cart = []

# ------------models-------------
# Q 6
class OrderRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    item_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0, le=20)
    delivery_address: str = Field(..., min_length=10)
    order_type: str = "delivery"

# Q 11
class NewMenuItem(BaseModel):
    name: str = Field(..., min_length=2)
    price: int = Field(..., gt=0)
    category: str = Field(..., min_length=2)
    is_available: bool = True

# Q 15
class CheckoutRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    delivery_address: str = Field(..., min_length=10)

# -----------helper functions-----------------
# Q 7
def find_menu_item(item_id: int):
    for item in menu:
        if item["id"] == item_id:
            return item
    return None


def calculate_bill(price: int, quantity: int,order_type="delivery"):
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

@app.get("/menu")
def get_menu():
    return {"menu": menu, "total": len(menu)}

# Q5
@app.get("/menu/summary")
def get_menu_summary():
    total=len(menu)
    available=len([i for i in menu if i["is_available"]])
    unavailable= total-available
    categories= list(set(i["category"] for i in menu))
    return {"total": total,
            "available": available,
            "unavailable": unavailable,
            "categories": categories
    }

# Q 9,10
@app.get("/menu/filter")
def filter_menu(
    category: Optional[str] = Query(None),
    max_price: Optional[int] = Query(None),
    is_available: Optional[bool] = Query(None)
):
    result = filter_menu_logic(category, max_price, is_available)
    return {"items": result, "count": len(result)}

# Q 16
@app.get("/menu/search")
def search_menu(keyword: str = Query(...)):

    result = [
        item for item in menu
        if keyword.lower() in item["name"].lower()
        or keyword.lower() in item["category"].lower()
    ]

    if not result:
        return {"message": "No items found"}

    return {"results": result, "total_found": len(result)}

# Q 17
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

# Q 18 - pagination
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

# Q 20
@app.get("/menu/browse")
def browse_menu(
    keyword: str = None,
    sort_by: str = "price",
    order: str = "asc",
    page: int = 1,
    limit: int = 4
):

    result = menu

    # filter
    if keyword:
        result = [
            i for i in result
            if keyword.lower() in i["name"].lower()
            or keyword.lower() in i["category"].lower()
        ]

    # sort
    reverse = True if order == "desc" else False
    result = sorted(result, key=lambda x: x[sort_by], reverse=reverse)

    # pagination
    start = (page - 1) * limit
    end = start + limit

    total = len(result)
    total_pages = (total + limit - 1) // limit

    return {
        "total": total,
        "total_pages": total_pages,
        "page": page,
        "items": result[start:end]
    }

# Q3
@app.get("/menu/{item_id}")
def get_menu_item(item_id: int):
    for item in menu:
        if item["id"] == item_id:
            return item
    return {"message": "Item not found"}


# Q4
@app.get("/orders")
def get_orders():
    return {"orders": orders,
            "total_orders": len(orders)}

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

# Q 8
@app.post("/orders")
def place_order(order: OrderRequest):
    global order_counter
    item = find_menu_item(order.item_id)
    if not item:
        return {"message": "Item not found"}
    if not item['is_available']:
        return {"message": "Item is not available"}
    
    total_price = calculate_bill(item['price'], order.quantity)

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

# Q 11
@app.post("/menu")
def add_menu_item(item: NewMenuItem, response: Response):
    # check duplicate (case-insensitive)
    for m in menu:
        if m["name"].lower() == item.name.lower():
            response.status_code = 400
            return {"error": "Item already exists"}

    new_id = len(menu) + 1

    new_item = {
        "id": new_id,
        "name": item.name,
        "price": item.price,
        "category": item.category,
        "is_available": item.is_available
    }

    menu.append(new_item)
    response.status_code = 201

    return new_item

# Q 12
@app.put("/menu/{item_id}")
def update_menu_item(
    item_id: int,
    price: int = Query(None),
    is_available: bool = Query(None),
    response: Response = Response
):
    item = find_menu_item(item_id)

    if not item:
        response.status_code = 404
        return {"error": "Item not found"}

    if price is not None:
        item["price"] = price

    if is_available is not None:
        item["is_available"] = is_available

    return item

# Q 13
@app.delete("/menu/{item_id}")
def delete_menu_item(item_id: int,response: Response):

    item = find_menu_item(item_id)

    if not item:
        response.status_code = 404
        return {"error": "Item not found"}

    menu.remove(item)

    return {"message": f"{item['name']} deleted successfully"}

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