class AccountDoesNotExistException(Exception):
    pass

class AccountIncorrectPasswordException(Exception):
    pass

class AccountLockedException(Exception):
    pass

class AccountBannedException(Exception):
    pass
