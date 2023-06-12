import logging
import time

import utilities.custom_logger as cl
from base.basepage import BasePage
from selenium.webdriver.wpewebkit.webdriver import WebDriver


class LoginPage(BasePage):

    log = cl.custom_logger(logging.DEBUG)

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.driver = driver

    # Locator
    _login_link = "SIGN IN"
    _email_input = "email"
    _password_input = "login-password"
    _login_button = "//button[.='Login']"
    _course_card = "dropdownMenu1"
    _error_banner = "//span[contains(@class, 'help-block')]"

    def click_on_login_link(self):
        self.element_click(self._login_link, "link_text")

    def enter_email(self, user_email: str):
        self.input(user_email, self._email_input)

    def enter_password(self, password: str):
        self.input(password, self._password_input)

    def click_login_button(self):
        self.element_click(self._login_button, "xpath")

    def login(self, user_name: str, password: str):
        self.wait_for_element(locator=self._login_link, locator_type="link_text", timeout=15)
        self.click_on_login_link()
        self.wait_for_element(locator=self._email_input, locator_type="name", timeout=15)
        self.enter_email(user_name)
        self.enter_password(password)
        self.click_login_button()

    def confirm_login_was_successful(self):
        is_present = self.is_element_present(self._course_card)

        return is_present

    def confirm_login_has_failed(self):
        is_present = self.is_element_present(self._error_banner, locator_type="xpath")

        return is_present

    def confirm_title_login_page(self):
        return self.verify_page_title("Google")

