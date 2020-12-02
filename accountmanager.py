class AccountManager:

    # 4.1.1 Required account information
    def verify_account(self, first_name, last_name, email_address, home_address, password):
        if first_name == None or last_name == None or home_address == None:
            return False

        return self.verify_email_address(email_address) and self.verify_password(password) and self.verify_email_does_not_exist_in_system(email_address)

    def verify_email_address(self, email_address):
        return None

    def verify_password(self, password):
        return None

    def verify_email_does_not_exist_in_system(self, email_address):
        return None

    def add_account(self, account):
        return None

    def unlock_account(self, activation_code):
        return None

    def send_password_reset_email(self, email):
        return None

    def send_email_verification_email(self, account):
        return None

    # actual implementation is expected to throw Exceptions
    def login(self, email, password):
        return None

    def get_account(self, account):
        return None

    def change_password(self, account, new_password):
        return None
