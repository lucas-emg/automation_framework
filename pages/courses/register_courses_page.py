import utilities.custom_logger as cl
import logging
from base.basepage import BasePage
from selenium.webdriver.common.by import By


class RegisterCoursesPage(BasePage):
    log = cl.custom_logger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    _search_box = "//input[@id='search']"
    _course = "//a[@href='/courses/javascript-for-beginners']"
    _all_courses_link = "//a[.='ALL COURSES']"
    _enroll_button = "//button[contains(text(), 'Enroll in Course')]"
    _cc_num = "cardnumber"
    _cc_exp = "exp-date"
    _cc_cvc = "cvc"
    _submit_button = "//button[contains(@class, 'zen-subscribe')][1]"
    _enroll_error_message = "//div[contains(@class, 'card-error')]//span"
    _my_courses_page_title = "//h1[contains(text(), 'My Courses')]"
    _all_courses_page_title = "//h1[contains(text(), 'All Courses')]"
    _search_button = "//button[contains(@class, 'find-course')]"

    def click_on_all_courses(self):
        self.element_click(locator=self._all_courses_link, locator_type="xpath")

    def search_course(self, course_name: str):
        self.wait_for_element(locator=self._all_courses_page_title, locator_type="xpath", timeout=5)
        self.input(data=course_name, locator=self._search_box, locator_type="xpath")
        self.element_click(locator=self._search_button, locator_type="xpath")

    def click_on_course_to_enroll(self, full_course_name: str):
        course = self.driver.find_element(by=By.XPATH, value=f"//h4[contains(text(), '{full_course_name}')]/ancestor::a")
        self.element_click(element=course)

    def enroll_on_course(self):
        self.wait_for_element(locator=self._enroll_button, locator_type="xpath")
        self.element_click(locator=self._enroll_button, locator_type="xpath")

    def verify_cc_failed(self):
        self.wait_for_element(locator=self._enroll_error_message, locator_type="xpath")
        return self.is_element_displayed(locator=self._enroll_error_message, locator_type="xpath")

    def wait_for_courses_page_to_load(self):
        self.wait_for_element(locator=self._my_courses_page_title, locator_type="xpath")

    def click_on_buy_button(self):
        self.wait_for_element(locator=self._submit_button, locator_type="xpath")
        self.element_click(locator=self._submit_button, locator_type="xpath")