from account import Account
from accountmanager import AccountManager
from emailutils import EmailUtils
from order import Order
from receipt import Receipt

accountManger = AccountManager()
emailUtils = EmailUtils()

EXISTING_ACCOUNT_EMAIL = 'existing@email.com'
STAFF_EMAIL = 'staff@email.com'
GUEST_EMAIL = 'test@email.com'

EXISTING_ACCOUNT = Account(EXISTING_ACCOUNT_EMAIL)
STAFF_ACCOUNT = Account(STAFF_EMAIL)
GUEST_ACCOUNT = Account(GUEST_EMAIL)


def test_user_has_account(self):
    # 4.4 Existing and Guest User Receipt

    assert emailUtils.account_exist(
        GUEST_EMAIL) == False, 'Account does not exist'


def test_user_does_not_have_account(self):
    # 4.4 Existing and Guest User Receipt

    assert emailUtils.account_exist(
        EXISTING_ACCOUNT_EMAIL) == True, 'Account does exist'


def test_send_receipt_to_guest(self):
    # 4.4.1 Guest User Receipt
    new_order = Order(GUEST_ACCOUNT, STAFF_ACCOUNT)

    order_receipt = Receipt(new_order)

    assert emailUtils.account_exist(
        EXISTING_ACCOUNT_EMAIL) == False, 'Account does not exist'

    assert emailUtils.send_receipt(
        GUEST_EMAIL, order_receipt) == True, 'Email has been sent'


def test_send_receipt_to_existing_account(self):
    # 4.4.2 Existing User Receipt
    assert emailUtils.account_exist(
        EXISTING_ACCOUNT_EMAIL) == True, 'Account does exist'

    new_order = Order(EXISTING_ACCOUNT, STAFF_ACCOUNT)

    order_receipt = Receipt(new_order)

    assert emailUtils.send_receipt(
        EXISTING_ACCOUNT_EMAIL, order_receipt) == True, 'Email has been sent'


def test_email_not_found(self):
    # 4.5.1.1 Email is not found
    assert emailUtils.get_customer_information(
        GUEST_EMAIL) == False, 'Can not find customer information'


def test_email_is_found(self):
    # 4.5.1.1 Email is found
    assert emailUtils.get_customer_information(
        EXISTING_ACCOUNT_EMAIL) == True, 'Customer information found'


def test_valid_shipping_address(self):
    # 4.5.1.3 Shipping Address Validation
    # Should there be a failing path?
    assert emailUtils.validate_shipping_address(
        EXISTING_ACCOUNT.address) == True, 'Shipping Address is valid'


def test_valid_payment_address(self):
    # 4.5.1.4 Payment Address Validation
    # Should there be a failing path?
    assert emailUtils.validate_payment_address(
        EXISTING_ACCOUNT.address) == True, 'Payment Address is valid'


def test_receipt_saved(self):
    # 4.6.1.2 Receipt Database Storage
    new_order = Order(EXISTING_ACCOUNT, STAFF_ACCOUNT)

    new_receipt = Receipt(new_order)

    assert emailUtils.save_receipt(
        new_receipt) == True, 'Receipt has been saved'


def test_payment_detail_saved(self):
    # 4.6.2 Payment Details
    # Possibly 4.6.3 as well?
    new_order = Order(EXISTING_ACCOUNT, STAFF_ACCOUNT)

    assert emailUtils.save_order(
        new_order) == True, 'Payment Information has been saved'


def test_customer_can_view_account(self):
    # 4.7.1 Personal Account Information

    assert accountManger.get_account(EXISTING_ACCOUNT) == True, 'Account found'


def test_view_specific_account_data(self):
    # 4.7.1.1

    # assert accountInformation == {'first_name': 'John', 'last_name': 'Doe',
                                #   'email_address': 'johndoe@email.com', 'address': 'address'}, 'Account information found'

    assert accountManger.get_account(
        EXISTING_ACCOUNT) == True, 'Account information found'
