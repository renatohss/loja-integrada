from uuid import uuid1

from manager.exceptions import ManagerItemAlreadyOnCartException, ManagerItemNotFoundException, \
    ManagerCartNotFoundException, ManagerInvalidItemQuantityException, ManagerInvalidDiscountValueException
from models.cart import Cart, Status, Item
from services.database.database import Database
from services.items.exceptions import ItemNotFoundException
from services.items.items import ItemManager


class CartManager:

    db = Database()

    def create_cart(self) -> Cart:
        cart_id = str(uuid1())
        cart = Cart(
            id=cart_id,
            status=Status.OPEN,
        )
        self.db.save(data=cart.to_json())
        return cart

    def get_cart(self, cart_id: str) -> Cart:
        cart = self.db.get(key=cart_id)
        if not cart:
            raise ManagerCartNotFoundException()
        return Cart.from_json(cart)

    def add_item(self, cart_id: str, sku: str, quantity: int) -> Cart:
        if quantity < 1:
            raise ManagerInvalidItemQuantityException()
        cart = self.get_cart(cart_id=cart_id)
        for item in cart.items:
            if item.sku == sku:
                raise ManagerItemAlreadyOnCartException()
        try:
            item_data = ItemManager().get_item(sku=sku)
        except ItemNotFoundException:
            raise ManagerItemNotFoundException()
        item = Item(
            sku=item_data["sku"],
            name=item_data["name"],
            price=item_data["price"],
            quantity=quantity,
            total_price=item_data["price"] * quantity
        )
        cart.add_item(item)
        self.db.save(data=cart.to_json())
        return cart

    def edit_item(self, cart_id: str, sku: str, quantity: int) -> Cart:
        if quantity < 1:
            raise ManagerInvalidItemQuantityException()
        cart = self.get_cart(cart_id=cart_id)
        cart.edit_item(sku=sku, quantity=quantity)
        self.db.save(data=cart.to_json())
        return cart

    def remove_item(self, cart_id: str, sku: str) -> Cart:
        cart = self.get_cart(cart_id=cart_id)
        cart.remove_item(sku=sku)
        self.db.save(data=cart.to_json())
        return cart

    def clear_cart_items(self, cart_id: str) -> Cart:
        cart = self.get_cart(cart_id=cart_id)
        cart.clear_items()
        return cart

    def set_discount(self, cart_id: str, discount: float):
        if discount < 0.0:
            raise ManagerInvalidDiscountValueException()
        cart = self.get_cart(cart_id=cart_id)
        cart.set_discount(discount=discount)
        self.db.save(data=cart.to_json())
        return cart
