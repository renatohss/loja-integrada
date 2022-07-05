from http import HTTPStatus


class ApiItemAlreadyOnCartException(Exception):
    def __init__(self):
        self.detail = "Item already exists on cart"
        self.status_code = HTTPStatus.CONFLICT


class ApiItemNotFoundException(Exception):
    def __init__(self):
        self.detail = "Item not found"
        self.status_code = HTTPStatus.NOT_FOUND


class ApiCartNotFoundException(Exception):
    def __init__(self):
        self.detail = "Cart not found"
        self.status_code = HTTPStatus.NOT_FOUND
