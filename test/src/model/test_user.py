import unittest
from src.model.user import User
from src.model.user import SecuredPassword
from src.model.exceptions.invalid_email_error import InvalidEmailError
from src.model.exceptions.invalid_phone_number_error import InvalidPhoneNumberError

class TestUnitsSecuredPassword(unittest.TestCase):
    def setUp(self) -> None:
        self.secured_password = SecuredPassword.from_raw_password("password1")

    def testEmailValidation(self):
        with self.assertRaises(InvalidEmailError):
            User(email="asd", phone_number="+54 9 11 1111-1111", fullname="Pepito",
                 photo="", secured_password=self.secured_password)

    def testPhoneValidation(self):
        with self.assertRaises(InvalidPhoneNumberError):
            User(email="giancafferata@hotmail.com", phone_number="asd", fullname="Pepito",
                 photo="", secured_password=self.secured_password)