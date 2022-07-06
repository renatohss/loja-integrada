import json

from services.items.exceptions import ItemNotFoundException


class ItemManager:

    @staticmethod
    def get_api():
        return json.load(open("items.json"))

    def get_item(self, sku: str):
        items_api = self.get_api()
        try:
            return items_api[sku]
        except KeyError:
            raise ItemNotFoundException()
