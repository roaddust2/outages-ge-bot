class AddressesNumExceeded(Exception):
    """Raises when user try to add more addresses than allowed"""
    pass


class AddressAlreadyExists(Exception):
    """Raises when user try to add existing address"""
    pass


class OutageAlreadySent(Exception):
    """Raises when user try to add existing address"""
    pass
