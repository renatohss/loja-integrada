from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Any

from pydantic import BaseModel

from services.items.exceptions import ItemNotFoundException


class Status(str, Enum):
    OPEN = "open"
    PAYMENT_PENDING = "payment_pending"
    CLOSED = "closed"


class AddItemRequest(BaseModel):
    cart_id: str
    sku: str
    quantity: int


@dataclass
class Item:
    sku: str
    name: str
    price: float
    quantity: int
    total_price: float = 0.0

    @classmethod
    def from_json(cls, raw: Dict[str, Any]) -> "Item":
        return cls(
            sku=raw["sku"],
            name=raw["name"],
            price=raw["price"],
            quantity=raw["quantity"],
            total_price=raw["price"] * raw["quantity"]
        )

    def to_json(self):
        return {
            "sku": self.sku,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "total_price": self.price * self.quantity
        }


@dataclass
class Cart:
    id: str
    status: Status
    items: List[Item] = field(default_factory=list)
    discount: float = 0.0
    original_price: float = 0.0
    total_price: float = 0.0

    @classmethod
    def from_json(cls, raw: Dict[str, Any]) -> "Cart":
        items = [Item.from_json(item) for item in raw["items"]]
        return cls(
            id=raw["id"],
            status=raw["status"],
            items=items,
            discount=raw["discount"],
            original_price=raw["original_price"],
            total_price=raw["total_price"]
        )

    def to_json(self) -> Dict[str, Any]:
        items = [item.to_json() for item in self.items]
        return {
            "id": self.id,
            "status": self.status,
            "items": items,
            "discount": self.discount,
            "original_price": self.original_price,
            "total_price": self.total_price
        }

    def calculate_total_price(self):
        total = 0
        for item in self.items:
            total += item.total_price
        self.original_price = total
        self.total_price = total - self.discount if total > self.discount else 0.0

    def add_item(self, item: Item):
        self.items.append(item)
        self.calculate_total_price()

    def edit_item(self, sku: str, quantity: int):
        sku_found = False
        for item in self.items:
            if item.sku == sku:
                item.quantity = quantity
                item.total_price = quantity * item.price
                sku_found = True
        self.calculate_total_price()
        if not sku_found:
            raise ItemNotFoundException()

    def remove_item(self, sku: str):
        sku_found = False
        for item in self.items:
            if item.sku == sku:
                self.items.pop(self.items.index(item))
                sku_found = True
        self.calculate_total_price()
        if not sku_found:
            raise ItemNotFoundException()

    def clear_items(self):
        self.items = []
        self.calculate_total_price()

    def set_discount(self, discount: float):
        self.discount = discount
        self.calculate_total_price()
