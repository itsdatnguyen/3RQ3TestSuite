from accountmanager import AccountManager
from account import Account
from accountexceptions import AccountBannedException, AccountDoesNotExistException, AccountLockedException, AccountIncorrectPasswordException
import pytest

def test_verify_account_is_valid():
    # 4.1.1 Required account information
    manager = AccountManager()
    assert manager.verify_account('Greg', 'Gregton', 'greg.ton@example.com',
                                  '46 Greg Ave', 'Password1') == True, 'Account information should be valid'

def test_verify_account_email_is_valid():
    # 4.1.1.1 Email validation
    manager = AccountManager()
    assert manager.verify_email_address(
        'greg.ton@example.com') == True, 'Email should be valid'

def test_verify_account_email_is_invalid():
    # 4.1.1.1 Email validation
    manager = AccountManager()
    assert manager.verify_email_address(
        'ton$gregexamplecom') == False, 'Email should not be valid'

def test_verify_existing_account_with_non_existing_account():
    # 4.1.1.2 Existing accounts
    email = 'test@wow.com'
    manager = AccountManager()

    assert manager.verify_email_does_not_exist_in_system(
        email) == True, 'Account does not exist within the system'

def test_verify_existing_account_with_existing_account():
    # 4.1.1.2 Existing accounts
    email = 'hey@example.com'
    manager = AccountManager()
    newAccount = Account(email)

    manager.add_account(newAccount)
    assert manager.verify_email_does_not_exist_in_system(
        email) == False, 'Account already exists within the system'

def test_verify_account_password_is_valid():
    # 4.1.1.3 Password validation
    manager = AccountManager()
    assert manager.verify_password(
        'Password1') == True, 'Password should be valid'

def test_verify_account_password_with_missing_upper_case_is_invalid():
    # 4.1.1.3 Password validation
    manager = AccountManager()
    assert manager.verify_password(
        'password1') == False, 'Password should not be valid'

def test_verify_account_password_with_missing_number_is_invalid():
    # 4.1.1.3 Password validation
    manager = AccountManager()
    assert manager.verify_password(
        'SupermanGuy') == False, 'Password should not be valid'

def test_default_account_is_locked():
    # 4.1.2 Locked default account state
    account = Account('test@gmail.com')
    assert account.is_locked == True, 'Account should be locked by default'

def test_password_verification_link_contains_correct_link():
    # 4.1.3.1 Password verification link
    manager = AccountManager()
    account = Account('myemail@email.com')

    manager.add_account(account)
    email_details = manager.send_email_verification_email(account)

    assert email_details != None and email_details.contains_correct_link() == True, 'Email verification email should contain a correct link'


def test_account_activation_link_is_valid():
    # 4.1.3.4 Account activation & 4.1.3.2 Link verification
    account = Account('test@gmail.com')
    manager = AccountManager()

    account.activation_code = 'Test123'
    manager.add_account(account)

    assert manager.unlock_account(
        account.activation_code) == True, 'Account should successfully be unlocked'

def test_account_activation_link_is_not_valid():
    # 4.1.3.3 Account activation - Invalid link & 4.1.3.2 Link verification
    account = Account('test@gmail.com')
    manager = AccountManager()

    account.activation_code = 'Test34'
    manager.add_account(account)

    assert manager.unlock_account(
        'invalidCode') == False, 'Account should not be unlocked'

def test_reset_password_is_successful():
    # 4.2 Password Reset
    account = Account('more@example.com')
    account.password = 'Password354'
    manager = AccountManager()

    manager.add_account(account)
    manager.change_password(account, 'newPassword454')

    assert manager.change_password(
        account, 'newPassword454') == True, 'Account password should be successfully changed'

def test_verify_password_reset_email_exists():
    # 4.2.1.1 Email validation
    manager = AccountManager()
    account = Account('test@exam.ple')

    manager.add_account(account)

    assert manager.verify_email_does_not_exist_in_system(
        account.email_address) == True, 'Email should exist in the system'

def test_verify_password_reset_email_does_not_exist():
    # 4.2.1.1 Email validation
    manager = AccountManager()
    assert manager.verify_email_does_not_exist_in_system(
        'ton$gregexamplecom') == False, 'Email should not exist in the system'

def test_send_password_reset_email_is_successful():
    # 4.2.1.2 Password reset email
    manager = AccountManager()
    account = Account('test@gmail.com')

    manager.add_account(account)

    assert manager.send_password_reset_email(
        account.email_address) == True, 'Password reset email should be sent successfully'

def test_send_password_reset_email_is_unsuccessful():
    # 4.2.1.2 Password reset email
    manager = AccountManager()

    assert manager.send_password_reset_email(
        'fake_email@example.com') == False, 'Password reset email should not be sent'

def test_login_account_does_not_exist_fails():
    # 4.3.1 Account does not exist
    manager = AccountManager()

    with pytest.raises(AccountDoesNotExistException):
        assert manager.login(
            'fake@email.com', 'wowza'), 'Expected login to fail due to a non-existing account'

def test_login_password_is_incorrect_fails():
    # 4.3.2 Password is incorrect
    manager = AccountManager()
    account = Account('test@gmail.com')
    account.password = 'truePassword1'
    account.is_locked = False
    account.is_banned = False

    manager.add_account(account)

    with pytest.raises(AccountIncorrectPasswordException):
        assert manager.login(
            account.email_address, 'wrongPassword2'), 'Expected login to fail due to incorrect password'

def test_login_account_is_locked_fails():
    # 4.3.3 Account is locked
    manager = AccountManager()
    account = Account('test@gmail.com')
    account.password = 'Password1'
    account.is_locked = True
    account.is_banned = False

    manager.add_account(account)

    with pytest.raises(AccountLockedException):
        assert manager.login(
            account.email_address, account.password), 'Expected login to fail due to locked account'

def test_login_account_is_banned_fails():
    # 4.3.4 Account is banned
    manager = AccountManager()
    account = Account('test@gmail.com')
    account.password = 'Password1'
    account.is_locked = False
    account.is_banned = True

    manager.add_account(account)

    with pytest.raises(AccountBannedException):
        assert manager.login(
            account.email_address, account.password), 'Expected login to fail due to banned account'

def test_login_account_with_correct_information_success():
    # 4.3.5 Login success
    manager = AccountManager()
    account = Account('cool@man.com')
    account.password = 'Coolio123'
    account.is_locked = False

    manager.add_account(account)

    assert manager.login(account.email_address,
                         account.password) == True, 'Expected login to succeed'

def test_kitchen_staff_view_all_accounts_success():
    # 4.8.1 Account view access
    manager = AccountManager()
    account = Account('cool@man.com')

    manager.add_account(account)

    account_data = manager.view_all_accounts('KitchenStaff')
    assert account_data[0].email_address == account.email_address, 'Expected to successfully retrieve all account data'

def test_kitchen_manager_view_all_accounts_success():
    # 4.8.1 Account view access
    manager = AccountManager()
    account = Account('yes@wow.com')

    manager.add_account(account)

    account_data = manager.view_all_accounts('KitchenManager')
    assert account_data[0].email_address == account.email_address, 'Expected to successfully retrieve all account data'

def test_customer_view_all_accounts_unsuccessful():
    # 4.8.1 Account view access
    manager = AccountManager()
    account = Account('test@see.ca')

    manager.add_account(account)

    account_data = manager.view_all_accounts('Customer')
    assert len(account_data) == 0, 'Expected to successfully retrieve all account data'

def test_view_all_accounts_successfully_contains_data():
    # 4.8.1.1 Viewable customer information
    manager = AccountManager()
    account = Account('test@see.ca')
    account.first_name = 'Bob'
    account.last_name = 'Tan'
    account.home_address = '56 Robertson Road'
    account.is_banned = False
    account.is_locked = False

    manager.add_account(account)

    account_data = manager.view_all_accounts('KitchenManager')
    retrieved_account = account_data[0]

    assert retrieved_account.first_name == account.first_name, 'Expected first name to match'
    assert retrieved_account.last_name == account.last_name, 'Expected last name to match'
    assert retrieved_account.email_address == account.email_address, 'Expected email address to match'
    assert retrieved_account.home_address == account.home_address, 'Expected home address to match'
    assert retrieved_account.is_banned == account.is_banned, 'Expected banned status to match'
    assert retrieved_account.is_locked == account.is_locked, 'Expected locked status to match'

def test_account_ban_successful():
    # 4.8.2 Account banning
    manager = AccountManager()
    account = Account('wow@example.ca')

    manager.add_account(account)
    manager.ban_account(account, True)

    assert manager.is_account_banned(account) == True, 'Expected account to be banned'

def test_account_unban_successful():
    # 4.8.2 Account banning
    manager = AccountManager()
    account = Account('wow@wqwer.ca')
    account.is_banned = True

    manager.add_account(account)
    manager.ban_account(account, False)

    assert manager.is_account_banned(account) == False, 'Expected account to be not banned'

def test_kitchen_manager_account_creation_successful():
    # 4.9.1 Management Account Creation
    manager = AccountManager()
  
    assert manager.admin_create_account('KitchenManager', 'newAdmin@hotmail.com', 'KitchenStaff') == True, 'Expected kitchen staff account to be created'

def test_kitchen_staff_account_creation_successful():
    # 4.9.1 Management Account Creation
    manager = AccountManager()
  
    assert manager.admin_create_account('KitchenStaff', 'newAdmin@hotmail.com', 'KitchenStaff') == False, 'Expected kitchen staff account to not be created'

def test_account_creation_with_kitchen_staff_role_successful():
    # 4.9.1.1 Account Type
    manager = AccountManager()
  
    assert manager.admin_create_account('KitchenManager', 'newAdmin@hotmail.com', 'KitchenStaff') == True, 'Expected kitchen staff account to be created'

def test_account_creation_with_kitchen_manager_role_successful():
    # 4.9.1.1 Account Type
    manager = AccountManager()
  
    assert manager.admin_create_account('KitchenManager', 'newAdmin@hotmail.com', 'KitchenManager') == True, 'Expected kitchen staff manager to be created'

def test_account_creation_with_customer_role_unsuccessful():
    # 4.9.1.1 Account Type
    manager = AccountManager()
  
    assert manager.admin_create_account('KitchenManager', 'newAdmin@hotmail.com', 'Customer') == False, 'Expected customer to not be created'