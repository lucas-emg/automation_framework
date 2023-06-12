import logging
import os.path
import time

import utilities.custom_logger as cl
from traceback import print_stack

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.wpewebkit.webdriver import WebDriver


class SeleniumDriver:

    log = cl.custom_logger(logging.DEBUG)

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def screenshot(self, result_message):
        """
        Takes screenshot of the current open web page
        """
        file_name = result_message + "." + str(round(time.time() * 1_000)) + ".png"
        screenshot_directory = "C:\\Users\\lucas\\workspace_python\\letskodeit\\screenshots\\"
        relative_file_name = screenshot_directory + file_name
        current_directory = os.path.dirname(__file__)
        destination_file_name = os.path.join(current_directory, relative_file_name)
        destination_directory = os.path.join(current_directory, screenshot_directory)

        try:
            if not os.path.exists(destination_directory):
                os.makedirs(destination_directory)
            self.driver.save_screenshot(destination_file_name)
            self.log.info(f"Screenshot saved to directory: {destination_file_name}")
        except:
            self.log.error("### Exception occurred")
            print_stack()

    def get_by_type(self, locator_type: str):
        locator_type = locator_type.lower()
        if locator_type == "id":
            return By.ID
        elif locator_type == "xpath":
            return By.XPATH
        elif locator_type == "name":
            return By.NAME
        elif locator_type == "css":
            return By.CSS_SELECTOR
        elif locator_type == "class_name":
            return By.CLASS_NAME
        elif locator_type == "link_text":
            return By.LINK_TEXT
        else:
            self.log.info(f'Locator type "{locator_type}" is not supported')
        return False

    def get_element(self, locator, locator_type: str = 'id') -> WebElement:
        element = None
        try:
            locator_type = locator_type.lower()
            by_type = self.get_by_type(locator_type)
            element = self.driver.find_element(by_type, locator)
            self.log.info(f"Element found with locator: {locator} locator_type: {locator_type}")
        except:
            self.log.info('Element not found with locator: {locator} locator_type: {locator_type}')

        return element

    def get_element_list(self, locator, locator_type: str = 'id') -> list[WebElement]:
        """
        New Method
        GEt list of elements
        """
        elements = None
        try:
            locator_type = locator_type.lower()
            by_type = self.get_by_type(locator_type)
            elements = self.driver.find_elements(by_type, locator)
            self.log.info("Element list found with locator: " + locator +
                          " and locator_type: " + locator_type)
        except:
            self.log.error("Element list not found found with locator: " + locator +
                           " and locator_type: " + locator_type)

        return elements

    def is_element_present(self, locator, locator_type='id'):
        element = None
        try:
            element = self.get_element(locator, locator_type)
            self.log.info("Element was found")
            if element is not None:
                return True
            else:
                return False
        except:
            self.log.info('Element was not found')
            return False

    def wait_for_element(self, locator, locator_type="id", timeout=10, poll_frequency=0.5):
        element = None

        try:
            by_type = self.get_by_type(locator_type)
            self.log.info("Waiting for maximum :: " + str(timeout) + " :: seconds for element to be clickable")
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=poll_frequency,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            element = wait.until(EC.visibility_of_element_located((by_type, locator)))
            self.log.info("Element appeared on the web page")
        except:
            self.log.info("Element did not appear on the web page")
            print_stack()

        return element

    def element_click(self, locator="", locator_type='id', element=None):
        try:
            if locator:
                element = self.get_element(locator, locator_type)
            element.click()
            self.log.info(f'Click on element with locator: {locator} locator_type: {locator_type}')
        except:
            self.log.info(f'Cannot click on the element with locator: {locator} locator_type: {locator_type}')
            print_stack()

    def input(self, data, locator="", locator_type='id', element=None):
        try:
            if locator:
                element = self.get_element(locator, locator_type)
            element.send_keys(data)
            self.log.info(f'Input data on element with locator: {locator} locator_type: {locator_type}')
        except:
            self.log.info(f'Cannot input data on the element with locator: {locator} locator_type: {locator_type}')
            print_stack()

    def get_text(self, locator='', locator_type='id', element=None, info=''):
        """
        New Method
        Get 'Text' on an element
        Either provide element or a combination of locator and locator_type
        """
        try:
            if locator:
                self.log.debug("In locator condition")
                element = self.get_element(locator, locator_type)
            self.log.debug("Before finding text")
            text = element.text
            self.log.debug("After finding text, size is: " + str(len(text)))
            if len(text) == 0:
                text = element.get_attribute("innerText")
            if len(text) != 0:
                self.log.info("Getting text form element :: " + info)
                self.log.info("The text is :: '" + text + "'")
                text = text.strip()
        except:
            self.log.error("Failed to get text from element :: " + info)
            print_stack()
            text = None

        return text

    def is_element_displayed(self, locator='', locator_type='id', element=None):
        is_displayed = False
        try:
            if locator:
                element = self.get_element(locator, locator_type)
            if element is not None:
                is_displayed = element.is_displayed()
                self.log.info("Element is displayed with locator: " + locator +
                              " and locator_type: " + locator_type)
            else:
                self.log.error("Element is not displayed with locator: " + locator +
                               " and locator_type: " + locator_type)
            return is_displayed
        except:
            self.log.error("Element was not found")
            return False

    def scroll_browser(self, direction="up"):
        if direction == "up":
            self.driver.execute_script("window.scrollBy(0, -1000);")
        if direction == "down":
            self.driver.execute_script("window.scrollBy(0, -1000);")