import time

from utilities.teststatus import TestStatus
from pages.home.login_page import LoginPage
import unittest
import pytest


@pytest.mark.usefixtures("one_time_setup", "set_up")
class LoginTests(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def classSetup(self, one_time_setup):
        self.login_page = LoginPage(self.driver)
        self.ts = TestStatus(self.driver)

    @pytest.mark.order(1)
    def test_invalid_login(self) -> None:
        time.sleep(3)
        self.login_page.login(user_name="asdasdasdasdasd", password='asdasdasdasdasd')
        confirm_login = self.login_page.confirm_login_has_failed()

        assert confirm_login is True

    @pytest.mark.order(2)
    def test_valid_login(self) -> None:
        self.login_page.login(user_name='test@email.com', password='abcabc')
        is_page_title = self.login_page.confirm_title_login_page()
        self.ts.mark(is_page_title, "Title is Incorrect")
        confirm_login = self.login_page.confirm_login_was_successful()

        self.ts.mark_final(test_name="test_valid_login",
                           result=confirm_login,
                           result_message="Login was not successful")
