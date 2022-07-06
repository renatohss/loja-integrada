class ManagerItemAlreadyOnCartException(Exception):
    pass


class ManagerItemNotFoundException(Exception):
    pass


class ManagerCartNotFoundException(Exception):
    pass


class ManagerInvalidItemQuantityException(Exception):
    pass


class ManagerInvalidDiscountValueException(Exception):
    pass
