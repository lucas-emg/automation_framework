from base.selenium_driver import SeleniumDriver
from utilities.util import Util


class BasePage(SeleniumDriver):

    def __init__(self, driver):
        super(BasePage, self).__init__(driver)
        self.driver = driver
        self.util = Util()

    def verify_page_title(self, page_title: str):
        if page_title in self.driver.title:
            return True
        else:
            return False
