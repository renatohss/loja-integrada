from uuid import uuid1

from manager.exceptions import ItemAlreadyOnCartException
from models.cart import Cart, Status, Item
from services.database.database import Database
from services.items.items import ItemManager


class CartManager:
    @staticmethod
    def create_cart() -> Cart:
        cart_id = str(uuid1())
        cart = Cart(
            id=cart_id,
            status=Status.OPEN,
        )
        Database().save(data=cart.to_json())
        return cart

    @staticmethod
    def get_cart(cart_id: str) -> Cart:
        cart = Database().get(key=cart_id)
        return Cart.from_json(cart)

    def add_item(self, cart_id: str, sku: str, quantity: int):
        cart = self.get_cart(cart_id=cart_id)
        for item in cart.items:
            if item.sku == sku:
                raise ItemAlreadyOnCartException()
        item_data = ItemManager().get_item(sku=sku)
        item = Item(
            sku=item_data["sku"],
            name=item_data["name"],
            price=item_data["price"],
            quantity=quantity,
            total_price=item_data["price"] * quantity

        )
        cart.add_item(item)
        cart.total_price += item_data["price"] * quantity
        Database().save(data=cart.to_json())
        return cart