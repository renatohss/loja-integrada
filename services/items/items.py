import json
from typing import Dict

from services.items.exceptions import ItemNotFoundException


class ItemManager:
    items_api: Dict = json.load(open("items.json"))

    def get_item(self, sku: str):
        try:
            return self.items_api[sku]
        except KeyError:
            raise ItemNotFoundException()
