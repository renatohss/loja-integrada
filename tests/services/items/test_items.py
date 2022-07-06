from unittest import mock

import pytest

from services.items.exceptions import ItemNotFoundException
from services.items.items import ItemManager


class TestItems:
    @pytest.fixture
    def mock_json_load(self):
        with mock.patch(
            "services.items.items.json.load"
        ) as mock_json_load:
            yield mock_json_load

    @pytest.fixture
    def mock_items_api(self):
        with mock.patch(
            "services.items.items.ItemManager.get_api"
        ) as mock_api:
            yield mock_api

    def test_should_get_item_api(self, mock_json_load):
        mock_json_load.return_value = {}
        items = ItemManager().get_api()
        assert items == {}

    def test_should_get_item(self, mock_items_api):
        mock_items_api.return_value = {
              "fake-sku": {
                "sku": "fake-sku",
                "name": "fake-name",
                "price": 10.0
              }
            }
        item = ItemManager().get_item(sku="fake-sku")
        assert item == {
                        "sku": "fake-sku",
                        "name": "fake-name",
                        "price": 10.0
        }

    def test_should_raise_not_found_exception(self, mock_items_api):
        mock_items_api.return_value = {}
        with pytest.raises(ItemNotFoundException):
            ItemManager().get_item(sku="wrong-sku")
