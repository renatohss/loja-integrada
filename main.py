from fastapi import FastAPI, Depends

from api.exceptions import ApiItemAlreadyOnCartException
from manager.cart import CartManager
from manager.exceptions import ItemAlreadyOnCartException
from models.cart import AddItemRequest

app = FastAPI()


@app.post("/cart")
def create_cart(manager: CartManager = Depends(CartManager)):
    cart = manager.create_cart()
    return cart


@app.get("/cart/{cart_id}")
def get_cart(cart_id: str, manager: CartManager = Depends(CartManager)):
    cart = manager.get_cart(cart_id=cart_id)
    return cart


@app.post("/cart/{cart_id}/items/{item_sku}")
def add_item(add_item_request: AddItemRequest, manager: CartManager = Depends(CartManager)):
    try:
        cart = manager.add_item(
            cart_id=add_item_request.cart_id,
            sku=add_item_request.sku,
            quantity=add_item_request.quantity
        )
        return cart
    except ItemAlreadyOnCartException:
        return ApiItemAlreadyOnCartException()


@app.put("/cart/{cart_id}/items/{item_sku}")
def edit_item(cart_id: str, sku: str):
    return "cart_with_items_updated"


@app.delete("/cart/{cart_id}/items/{item_sku}")
def remove_item(cart_id: str, sku: str):
    return "cart_with_items_updated"


@app.delete("/cart/{cart_id}/clear")
def clear_cart(cart_id: str):
    return "cart_with_no_items"
