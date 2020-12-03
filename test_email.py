from account import Account
from accountmanager import AccountManager
from emailutils import EmailUtils
from order import Order
from ordermanager import OrderManager
from receipt import Receipt
from receiptmanager import ReceiptManager

accountManger = AccountManager()
emailUtils = EmailUtils()


def test_user_has_account():
    # 4.4 Existing and Guest User Receipt

    assert emailUtils.account_exist(
        'guest@gmail.com') == False, 'Account does not exist'


def test_user_does_not_have_account():
    # 4.4 Existing and Guest User Receipt
    manager = AccountManager()
    account = Account('guest@gmail.com')

    manager.add_account(account)

    assert emailUtils.account_exist(
        'existing@gmail.com') == True, 'Account does exist'


def test_send_receipt_to_guest():
    # 4.4.1 Guest User Receipt
    manager = AccountManager()
    account = Account('guest@gmail.com')

    staff_account = Account('staff@gmail.com')

    manager.add_account(account)
    manager.add_account(staff_account)

    new_order = Order(account, staff_account)

    order_receipt = Receipt(new_order)

    assert emailUtils.account_exist(
        account) == False, 'Account does not exist'

    assert emailUtils.send_receipt(
        'guest@gmail.com', order_receipt) == True, 'Email has been sent'


def test_email_has_link_to_account_creation_page():
    # 4.4.1.1 Guest Account Creation
    manager = AccountManager()
    account = Account('guest@gmail.com')

    staff_account = Account('staff@gmail.com')

    manager.add_account(account)
    manager.add_account(staff_account)

    new_order = Order(account, staff_account)

    order_receipt = Receipt(new_order)

    assert emailUtils.validate_receipt_content(
        order_receipt) == True, 'Redirect Link Found'


def test_send_receipt_to_existing_account():
    # 4.4.2 Existing User Receipt
    manager = AccountManager()
    account = Account('existing@gmail.com')

    staff_account = Account('staff@gmail.com')

    manager.add_account(account)
    manager.add_account(staff_account)

    assert emailUtils.account_exist(
        'existing@gmail.com') == True, 'Account does exist'

    new_order = Order(account, staff_account)

    order_receipt = Receipt(new_order)

    assert emailUtils.send_receipt(
        'existing@gmail.com', order_receipt) == True, 'Email has been sent'


def test_email_receipt_after_order_fails():
    # 4.5 Email Receipt after Order
    manager = AccountManager()
    account = Account('guest@gmail.com')

    manager.add_account(account)

    assert emailUtils.send_receipt(
        account.email_address, {}) == False, 'No Receipt Found, Email has not been sent'


def test_account_information_in_email_content():
    # 4.5.1 Email Information for Account
    manager = AccountManager()
    account = Account('guest@gmail.com')

    staff_account = Account('staff@gmail.com')

    manager.add_account(account)
    manager.add_account(staff_account)

    assert emailUtils.account_exist(
        'existing@gmail.com') == True, 'Account does exist'

    new_order = Order(account, staff_account)

    order_receipt = Receipt(new_order)
    order_receipt.content = 'Valid Email Content'

    assert emailUtils.validate_receipt_content(
        order_receipt.content) == True, 'Email Content is valid'


def test_email_not_found():
    # 4.5.1.1 Email is not found
    assert emailUtils.get_customer_information(
        'guest@gmail.com') == False, 'Can not find customer information'


def test_email_is_found():
    # 4.5.1.2 Email is found
    manager = AccountManager()
    account = Account('existing@gmail.com')

    manager.add_account(account)

    assert emailUtils.get_customer_information(
        'existing@gmail.com') == True, 'Customer information found'


def test_valid_shipping_address():
    # 4.5.1.3 Shipping Address Validation
    manager = AccountManager()
    account = Account('existing@gmail.com')
    account.address = '10 valid drive'

    manager.add_account(account)

    assert emailUtils.validate_shipping_address(
        account.address) == True, 'Shipping Address is valid'


def test_invalid_shipping_address():
    # 4.5.1.3 Shipping Address Validation
    manager = AccountManager()
    account = Account('guest@gmail.com')
    account.address = '10 not valid 10 drive'

    manager.add_account(account)

    assert emailUtils.validate_shipping_address(
        account.address) == False, 'Shipping Address is invalid'


def test_valid_payment_address():
    # 4.5.1.4 Payment Address Validation
    manager = AccountManager()
    account = Account('existing@gmail.com')
    account.address = '10 valid lane'

    manager.add_account(account)

    assert emailUtils.validate_payment_address(
        account.address) == True, 'Payment Address is valid'


def test_invalid_payment_address():
    # 4.5.1.4 Payment Address Validation
    manager = AccountManager()
    account = Account('existing@gmail.com')
    account.address = '10 invalid 10 drive'

    manager.add_account(account)

    assert emailUtils.validate_payment_address(
        account.address) == True, 'Payment Address is invalid'


def test_save_receipt_record():
    # 4.6 Save Receipt Record
    receiptManager = ReceiptManager()
    manager = AccountManager()
    account = Account('guest@gmail.com')

    staff_account = Account('staff@gmail.com')

    manager.add_account(account)
    manager.add_account(staff_account)

    assert emailUtils.account_exist(
        'existing@gmail.com') == True, 'Account does exist'

    new_order = Order(account, staff_account)

    order_receipt = Receipt(new_order)
    receiptManager.add_receipt(order_receipt)

    assert receiptManager.get_receipt_information(order_receipt)


def test_get_customer_information():
    # 4.6.1 Customer Information
    manager = AccountManager()
    account = Account('guest@gmail.com')

    manager.add_account(account)

    assert emailUtils.get_account(
        account) == True, 'Account information found'


def test_receipt_saved():
    # 4.6.1.2 Receipt Database Storage
    receiptManager = ReceiptManager()
    new_order = Order(EXISTING_ACCOUNT, STAFF_ACCOUNT)

    new_receipt = Receipt(new_order)

    assert receiptManager.add_receipt(
        new_receipt) == True, 'Receipt has been saved'


def test_payment_detail_saved_for_existing_account():
    # 4.6.2 Complete Sale Transaction Details for Existing Account
    manager = AccountManager()
    account = Account('existing@gmail.com')
    account.address = 'address'
    account.payment_method = 'visa'

    manager.add_account(account)

    assert emailUtils.save_order(
        account) == True, 'Payment Information has been saved'


def test_payment_detail_saved_for_guest_account():
    # 4.6.2 Complete Sale Transaction Details for Guest Account
    manager = AccountManager()
    account = Account('guest@gmail.com')
    account.address = 'address'
    account.payment_method = 'visa'

    manager.add_account(account)

    assert emailUtils.save_order(
        account) == True, 'Payment Information has been saved'


def test_complete_sale_transaction_details_for_existing_account():
    # 4.6.3 Complete Sale Transaction Details for Existing Account
    manager = AccountManager()
    account = Account('existing@gmail.com')
    account.address = 'address'
    account.payment_method = 'visa'

    staff_account = Account('staff@gmail.com')

    manager.add_account(account)
    manager.add_account(staff_account)

    new_order = Order(account, staff_account)

    assert emailUtils.save_order(
        new_order) == True, 'Transaction Information has been saved'


def test_complete_sale_transaction_details_for_guest_account():
    # 4.6.3 Complete Sale Transaction Details for Guest Account
    manager = AccountManager()
    account = Account('guest@gmail.com')
    account.address = 'address'
    account.payment_method = 'visa'

    staff_account = Account('staff@gmail.com')

    manager.add_account(account)
    manager.add_account(staff_account)

    new_order = Order(account, staff_account)

    assert emailUtils.save_order(
        new_order) == True, 'Transaction Information has been saved'


def test_customer_can_view_account():
    # 4.7.1 Personal Account Information
    manager = AccountManager()
    account = Account('existing@gmail.com')
    account.address = 'address'
    account.payment_method = 'visa'

    manager.add_account(account)

    assert accountManger.get_account(account) == True, 'Account found'


def test_can_view_specific_account_data_success():
    # 4.7.1.1 Viewable Customer Information
    manager = AccountManager()
    account = Account('existing@gmail.com')

    manager.add_account(account)

    assert accountManger.get_account(
        account) == True, 'Account information found'


def test_can_view_specific_account_data_fails():
    # 4.7.1.1 Viewable Customer Information
    account = Account('guest@gmail.com')

    assert accountManger.get_account(
        account) == True, 'Account information not found'


def test_modify_account_information():
    # 4.7.2.1 Modifiable Information
    manager = AccountManager()
    account = Account('existing@gmail.com')
    account.first_name = 'John'
    account.last_name = 'Doe'
    account.address = '10 Valid Drive'

    manager.add_account(account)

    assert manager.change_personal_information(
        account, 'Joe', 'Schmoe', 'newemail@gmail.com', '10 Change Lane') == True, 'Account information successfully changed'


def test_view_customer_orders():
    # 4.7.3.1 Order Information
    orderManager = OrderManager()
    manager = AccountManager()
    account = Account('guest@gmail.com')

    staff_account = Account('staff@gmail.com')

    manager.add_account(account)
    manager.add_account(staff_account)

    new_order = Order(account, staff_account)
    orderManager.add_order(new_order)

    all_orders = orderManager.view_all_orders(account)

    assert all_orders[0].customer == account, 'Orders found'


def test_view_receipt_as_staff():
    # 4.9.1 Receipt View Access
    orderManager = OrderManager()
    manager = AccountManager()
    receiptManager = ReceiptManager()

    account = Account('guest@gmail.com')
    staff_account = Account('staff@gmail.com')

    manager.add_account(account)
    manager.add_account(staff_account)

    new_order = Order(account, staff_account)
    orderManager.add_order(new_order)

    order_receipt = Receipt(new_order)
    receiptManager.add_receipt(order_receipt)

    all_receipts = receiptManager.get_all_receipts(staff_account)

    assert all_receipts[0].received_by == staff_account, 'Receipt for Staff found'
