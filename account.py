class Account:
    def __init__(self, email_address):
        self.is_locked = True
        self.email_address = email_address
        self.activation_code = None
        self.password = None
        self.is_banned = False
        self.address = None
        self.first_name = None
        self.last_name = None
        self.home_address = None
