from fastapi import FastAPI, Depends

from api.exceptions import ApiItemAlreadyOnCartException, ApiItemNotFoundException, ApiCartNotFoundException
from manager.cart import CartManager
from manager.exceptions import ManagerItemAlreadyOnCartException, ManagerItemNotFoundException, \
    ManagerCartNotFoundException
from models.cart import AddItemRequest

app = FastAPI()


@app.post("/cart")
def create_cart(manager: CartManager = Depends(CartManager)):
    return manager.create_cart()


@app.get("/cart/{cart_id}")
def get_cart(cart_id: str, manager: CartManager = Depends(CartManager)):
    try:
        return manager.get_cart(cart_id=cart_id)
    except ManagerCartNotFoundException:
        return ApiCartNotFoundException()


@app.post("/cart/{cart_id}/items/{item_sku}")
def add_item(add_item_request: AddItemRequest, manager: CartManager = Depends(CartManager)):
    try:
        return manager.add_item(
            cart_id=add_item_request.cart_id,
            sku=add_item_request.sku,
            quantity=add_item_request.quantity
        )
    except ManagerItemAlreadyOnCartException:
        return ApiItemAlreadyOnCartException()
    except ManagerItemNotFoundException:
        return ApiItemNotFoundException()


@app.put("/cart/{cart_id}/items/{item_sku}/{quantity}")
def edit_item(cart_id: str, sku: str, quantity: int, manager: CartManager = Depends(CartManager)):
    try:
        return manager.edit_item(cart_id=cart_id, sku=sku, quantity=quantity)
    except ManagerItemNotFoundException:
        return ApiItemNotFoundException()


@app.delete("/cart/{cart_id}/items/{item_sku}")
def remove_item(cart_id: str, sku: str):
    return "cart_with_items_updated"


@app.delete("/cart/{cart_id}/clear")
def clear_cart(cart_id: str):
    return "cart_with_no_items"
