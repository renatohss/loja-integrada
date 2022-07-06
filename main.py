from fastapi import FastAPI, Depends

from api.exceptions import ApiItemAlreadyOnCartException, ApiItemNotFoundException, ApiCartNotFoundException, \
    ApiInvalidItemQuantityException
from manager.cart import CartManager
from manager.exceptions import ManagerItemAlreadyOnCartException, ManagerItemNotFoundException, \
    ManagerCartNotFoundException, ManagerInvalidItemQuantityException
from models.cart import AddItemRequest
from services.items.exceptions import ItemNotFoundException

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
    except ItemNotFoundException:
        return ApiItemNotFoundException()
    except ManagerInvalidItemQuantityException:
        return ApiInvalidItemQuantityException()


@app.put("/cart/{cart_id}/items/{item_sku}/{quantity}")
def edit_item(cart_id: str, sku: str, quantity: int, manager: CartManager = Depends(CartManager)):
    try:
        return manager.edit_item(cart_id=cart_id, sku=sku, quantity=quantity)
    except ItemNotFoundException:
        return ApiItemNotFoundException()
    except ManagerInvalidItemQuantityException:
        return ApiInvalidItemQuantityException()


@app.delete("/cart/{cart_id}/items/{item_sku}")
def remove_item(cart_id: str, sku: str, manager: CartManager = Depends(CartManager)):
    try:
        return manager.remove_item(cart_id=cart_id, sku=sku)
    except ItemNotFoundException:
        return ApiItemNotFoundException()
    except ManagerCartNotFoundException:
        return ApiCartNotFoundException()


@app.delete("/cart/{cart_id}/clear_items")
def clear_cart(cart_id: str, manager: CartManager = Depends(CartManager)):
    try:
        return manager.clear_cart_items(cart_id=cart_id)
    except ManagerCartNotFoundException:
        return ApiCartNotFoundException()


@app.patch("/cart/{cart_id}/set_discount/{discount}")
def set_discount(cart_id: str, discount: float, manager: CartManager = Depends(CartManager)):
    try:
        return manager.set_discount(cart_id=cart_id, discount=discount)
    except ManagerCartNotFoundException:
        return ApiCartNotFoundException()
