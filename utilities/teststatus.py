import logging

from base.selenium_driver import SeleniumDriver
from selenium.webdriver.wpewebkit.webdriver import WebDriver
from utilities.custom_logger import custom_logger


class TestStatus(SeleniumDriver):

    log = custom_logger(logging.INFO)

    def __init__(self, driver: WebDriver):
        """
        Initiates CheckPoint class
        """
        super(TestStatus, self).__init__(driver)
        self.result_list = []

    def set_result(self, result, result_message):
        try:
            if result is not None:
                if result:
                    self.result_list.append("PASS")
                    self.log.info("### VERIFICATION SUCCESSFUL :: + " + result_message)
                else:
                    self.result_list.append("FAIL")
                    self.log.error("### VERIFICATION FAILED :: + " + result_message)
                    self.screenshot(result_message)
            else:
                self.result_list.append("FAIL")
                self.log.error("### VERIFICATION FAILED :: + " + result_message)
                self.screenshot(result_message)
        except Exception as e:
            self.result_list.append("FAIL")
            self.log.error("### EXCEPTION: " + str(e))
            self.screenshot(result_message)

    def mark(self, result, result_message):
        """
        Mark the result of the verification point in a test case
        """
        self.set_result(result, result_message)

    def mark_final(self, test_name, result, result_message):
        """
        Mark the final result of the verification point in a test case
        This needs to be called at least once in a test case
        This should be final status of the test case
        """
        self.set_result(result, result_message)

        if "FAIL" in self.result_list:
            self.log.error(test_name + " ### TEST FAILED")
            self.result_list.clear()
            assert True is False
        else:
            self.log.info(test_name + " ### TEST SUCCESSFUL")
            self.result_list.clear()
            assert True
