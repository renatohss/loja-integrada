from unittest import mock

import pytest

from manager.cart import CartManager
from manager.exceptions import (
    ManagerCartNotFoundException,
    ManagerInvalidItemQuantityException,
    ManagerItemAlreadyOnCartException,
    ManagerItemNotFoundException, ManagerInvalidDiscountValueException
)
from models.cart import Cart, Status, Item
from services.items.exceptions import ItemNotFoundException


class TestCartManager:

    @pytest.fixture
    def mock_cart_database_save(self):
        with mock.patch(
            "manager.cart.Database.save"
        ) as db_mock:
            yield db_mock

    @pytest.fixture
    def mock_cart_database_get(self):
        with mock.patch(
            "manager.cart.Database.get"
        ) as db_mock:
            yield db_mock

    @pytest.fixture
    def mock_cart_json(self):
        return {
            "id": "fake-id",
            "status": "open",
            "items": [{
                "sku": "1",
                "name": "fake-item",
                "price": 10.0,
                "quantity": 2,
                "total_price": 20.0
            }],
            "discount": 5.0,
            "original_price": 20.0,
            "total_price": 15.0,
        }

    @pytest.fixture
    def mock_get_cart(self):
        with mock.patch(
            "manager.cart.CartManager.get_cart"
        ) as mock_get_cart:
            yield mock_get_cart

    @pytest.fixture
    def mock_get_cart_response(self):
        return Cart(
            id="fake-id",
            status=Status.OPEN.value,
            items=[Item(
                sku="fake-sku",
                name="fake-name",
                price=10.0,
                quantity=2,
                total_price=20.0
            )],
            discount=5.0,
            original_price=20.0,
            total_price=15.0
        )

    @pytest.fixture
    def mock_item_manager_get_item(self):
        with mock.patch(
            "manager.cart.ItemManager.get_item"
        ) as mock_items:
            yield mock_items

    @pytest.fixture
    def mock_item_json(self):
        return {
            "sku": "2",
            "name": "another-fake-item",
            "price": 10.0
        }

    def test_should_create_cart(self, mock_cart_database_save):
        cart = CartManager().create_cart()
        mock_cart_database_save.assert_called_once()
        assert isinstance(cart, Cart)

    def test_should_get_cart(self, mock_cart_database_get, mock_cart_json):
        mock_cart_database_get.return_value = mock_cart_json
        cart = CartManager().get_cart(cart_id="fake-id")
        item = mock_cart_json["items"][0]
        assert cart == Cart(
            id=mock_cart_json["id"],
            status=mock_cart_json["status"],
            items=[Item(
                sku=item["sku"],
                name=item["name"],
                price=item["price"],
                quantity=item["quantity"],
                total_price=item["total_price"]
            )],
            discount=mock_cart_json["discount"],
            original_price=mock_cart_json["original_price"],
            total_price=mock_cart_json["total_price"]

        )

    def test_should_raise_exception_when_cart_not_found(self, mock_cart_database_get):
        mock_cart_database_get.return_value = None
        with pytest.raises(ManagerCartNotFoundException):
            CartManager().get_cart(cart_id="fake-id")

    def test_should_add_item(
            self,
            mock_get_cart,
            mock_cart_database_save,
            mock_item_manager_get_item,
            mock_get_cart_response,
            mock_item_json
    ):
        mock_get_cart.return_value = mock_get_cart_response
        mock_item_manager_get_item.return_value = mock_item_json
        cart = CartManager().add_item(cart_id="fake-id", sku="2", quantity=1)
        mock_cart_database_save.assert_called_once()
        assert cart == Cart(id='fake-id',
                            status='open',
                            items=[
                                Item(sku='fake-sku',
                                     name='fake-name',
                                     price=10.0,
                                     quantity=2,
                                     total_price=20.0),
                                Item(sku=mock_item_json["sku"],
                                     name=mock_item_json["name"],
                                     price=mock_item_json["price"],
                                     quantity=1,
                                     total_price=10.0)],
                            discount=5.0,
                            original_price=30.0,
                            total_price=25.0)

    def test_should_raise_invalid_quantity_exception_on_add_item(self):
        with pytest.raises(ManagerInvalidItemQuantityException):
            CartManager().add_item(cart_id="fake-id", sku="fake-sku", quantity=0)

    def test_should_raise_already_on_cart_exception_on_add_item(
            self,
            mock_get_cart,
            mock_get_cart_response,
    ):
        mock_get_cart.return_value = mock_get_cart_response
        with pytest.raises(ManagerItemAlreadyOnCartException):
            CartManager().add_item(cart_id="fake-id", sku="fake-sku", quantity=1)

    def test_should_raise_item_not_found_exception_on_add_item(
            self,
            mock_get_cart,
            mock_get_cart_response,
            mock_item_manager_get_item,
    ):
        mock_get_cart.return_value = mock_get_cart_response
        mock_item_manager_get_item.side_effect = ItemNotFoundException
        with pytest.raises(ManagerItemNotFoundException):
            CartManager().add_item(cart_id="fake-id", sku="wrong-sku", quantity=1)

    def test_should_edit_item(
            self,
            mock_get_cart,
            mock_get_cart_response,
            mock_cart_database_save,

    ):
        mock_get_cart.return_value = mock_get_cart_response
        cart = CartManager().edit_item(cart_id="fake-id", sku="fake-sku", quantity=10)
        mock_cart_database_save.assert_called_once()
        assert cart == Cart(
            id='fake-id',
            status='open',
            items=[Item(sku='fake-sku',
                        name='fake-name',
                        price=10.0,
                        quantity=10,
                        total_price=100.0)],
            discount=5.0,
            original_price=100.0,
            total_price=95.0)

    def test_should_raise_invalid_quantity_exception_on_edit_item(self):
        with pytest.raises(ManagerInvalidItemQuantityException):
            CartManager().edit_item(cart_id="fake-id", sku="fake-sku", quantity=0)

    def test_should_raise_item_not_found_exception_on_edit_item(
            self,
            mock_get_cart,
            mock_get_cart_response
    ):
        mock_get_cart.return_value = mock_get_cart_response
        with pytest.raises(ItemNotFoundException):
            CartManager().edit_item(cart_id="fake-id", sku="wrong-sku", quantity=1)

    def test_should_remove_item(
            self,
            mock_get_cart,
            mock_get_cart_response,
            mock_cart_database_save
    ):
        mock_get_cart.return_value = mock_get_cart_response
        cart = CartManager().remove_item(cart_id="fake-id", sku="fake-sku")
        mock_cart_database_save.assert_called_once()
        assert cart == Cart(
            id='fake-id',
            status='open',
            items=[],
            discount=5.0,
            original_price=0,
            total_price=0.0
        )

    def test_should_raise_item_not_found_exception_on_remove_item(
            self,
            mock_get_cart,
            mock_get_cart_response
    ):
        mock_get_cart.return_value = mock_get_cart_response
        with pytest.raises(ItemNotFoundException):
            CartManager().remove_item(cart_id="fake-id", sku="wrong-sku")

    def test_should_clear_cart_items(self, mock_get_cart, mock_get_cart_response):
        mock_get_cart.return_value = mock_get_cart_response
        cart = CartManager().clear_cart_items(cart_id="fake-id")
        assert cart.items == []

    def test_should_set_discount(
            self,
            mock_get_cart,
            mock_get_cart_response,
            mock_cart_database_save
    ):
        mock_get_cart.return_value = mock_get_cart_response
        cart = CartManager().set_discount(cart_id="fake-id", discount=10.0)
        mock_cart_database_save.assert_called_once()
        assert cart.discount == 10.0
        assert cart.total_price == 10.0
        assert cart.original_price == 20.0

    def test_should_raise_invalid_discount_exception_on_set_discount(self):
        with pytest.raises(ManagerInvalidDiscountValueException):
            CartManager().set_discount(cart_id="fake-id", discount=-5.0)
