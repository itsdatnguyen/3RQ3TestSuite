from accountmanager import AccountManager
from account import Account
from accountexceptions import AccountBannedException, AccountDoesNotExistException, AccountLockedException, AccountIncorrectPasswordException
import pytest

# 4.1.1 Required account information
def test_verify_account_is_valid():
    manager = AccountManager()
    assert manager.verify_account('Greg', 'Gregton', 'greg.ton@example.com', '46 Greg Ave', 'Password1') == True, 'Account information should be valid'

# 4.1.1.1 Email validation
def test_verify_account_email_is_valid():
    manager = AccountManager()
    assert manager.verify_email_address('greg.ton@example.com') == True, 'Email should be valid'

# 4.1.1.1 Email validation
def test_verify_account_email_is_invalid():
    manager = AccountManager()
    assert manager.verify_email_address('ton$gregexamplecom') == False, 'Email should not be valid'

# 4.1.1.1 Existing accounts
def test_verify_existing_account_with_non_existing_account():
    email = 'test@wow.com'
    manager = AccountManager()

    assert manager.verify_email_does_not_exist_in_system(email) == True, 'Account does not exist within the system'

# 4.1.1.1 Existing accounts
def test_verify_existing_account_with_existing_account():
    email = 'hey@example.com'
    manager = AccountManager()
    newAccount = Account(email)

    manager.add_account(newAccount)
    assert manager.verify_email_does_not_exist_in_system(email) == False, 'Account already exists within the system'

# 4.1.1.3 Password validation
def test_verify_account_password_is_valid():
    manager = AccountManager()
    assert manager.verify_password('Password1') == True, 'Password should be valid'

# 4.1.1.3 Password validation
def test_verify_account_password_with_missing_upper_case_is_invalid():
    manager = AccountManager()
    assert manager.verify_password('password1') == False, 'Password should not be valid'

# 4.1.1.3 Password validation
def test_verify_account_password_with_missing_number_is_invalid():
    manager = AccountManager()
    assert manager.verify_password('SupermanGuy') == False, 'Password should not be valid'

# 4.1.2 Locked default account state
def test_default_account_is_locked():
    account = Account('test@gmail.com')
    assert account.is_locked == True, 'Account should be locked by default'

# 4.1.3.4 Account activation
def test_account_activation_link_is_valid():
    account = Account('test@gmail.com')
    manager = AccountManager()

    account.activation_code = 'Test123'
    manager.add_account(account)

    assert manager.unlock_account(account.activation_code) == True, 'Account should successfully be unlocked'

# 4.1.3.3 Account activation - Invalid link
def test_account_activation_link_is_not_valid():
    account = Account('test@gmail.com')
    manager = AccountManager()

    account.activation_code = 'Test34'
    manager.add_account(account)

    assert manager.unlock_account('invalidCode') == False, 'Account should not be unlocked'

# 4.2.1.1 Email validation
def test_verify_password_reset_email_exists():
    manager = AccountManager()
    account = Account('test@exam.ple')

    manager.add_account(account)

    assert manager.verify_email_does_not_exist_in_system(account.email_address) == True, 'Email should exist in the system'

# 4.1.1.1 Email validation
def test_verify_password_reset_email_does_not_exist():
    manager = AccountManager()
    assert manager.verify_email_does_not_exist_in_system('ton$gregexamplecom') == False, 'Email should not exist in the system'

# 4.2.1.2 Password reset email
def test_send_password_reset_email_is_successful():
    manager = AccountManager()
    account = Account('test@gmail.com')

    manager.add_account(account)

    assert manager.send_password_reset_email(account.email_address) == True, 'Password reset email should be sent successfully'

# 4.2.1.2 Password reset email
def test_send_password_reset_email_is_unsuccessful():
    manager = AccountManager()

    assert manager.send_password_reset_email('fake_email@example.com') == False, 'Password reset email should not be sent'

# 4.3.2.1 Account does not exist
def test_login_account_does_not_exist_fails():
    manager = AccountManager()

    with pytest.raises(AccountDoesNotExistException):
        assert manager.login('fake@email.com', 'wowza'), 'Expected login to fail due to a non-existing account'

# 4.3.2.2 Password is incorrect
def test_login_password_is_incorrect_fails():
    manager = AccountManager()
    account = Account('test@gmail.com')
    account.password = 'truePassword1'
    account.is_locked = False
    account.is_banned = False

    manager.add_account(account)

    with pytest.raises(AccountIncorrectPasswordException):
        assert manager.login(account.email_address, 'wrongPassword2'), 'Expected login to fail due to incorrect password'

# 4.3.2.3 Account is locked
def test_login_account_is_locked_fails():
    manager = AccountManager()
    account = Account('test@gmail.com')
    account.password = 'Password1'
    account.is_locked = True
    account.is_banned = False

    manager.add_account(account)

    with pytest.raises(AccountLockedException):
        assert manager.login(account.email_address, account.password), 'Expected login to fail due to locked account'

# 4.3.2.4 Account is banned
def test_login_account_is_banned_fails():
    manager = AccountManager()
    account = Account('test@gmail.com')
    account.password = 'Password1'
    account.is_locked = False
    account.is_banned = True

    manager.add_account(account)

    with pytest.raises(AccountBannedException):
        assert manager.login(account.email_address, account.password), 'Expected login to fail due to banned account'

# 4.3.2.5 Login success
def test_login_account_with_correct_information_success():
    manager = AccountManager()
    account = Account('cool@man.com')
    account.password = 'Coolio123'
    account.is_locked = False

    manager.add_account(account)

    assert manager.login(account.email_address, account.password) == True, 'Expected login to succeed'