from http import HTTPStatus


class ApiItemAlreadyOnCartException(Exception):
    def __init__(self):
        self.detail = "Item already exists on cart"
        self.status_code = HTTPStatus.CONFLICT
