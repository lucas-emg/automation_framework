from utilities.teststatus import TestStatus
from pages.courses.register_courses_page import RegisterCoursesPage
from pages.home.login_page import LoginPage
import unittest
import pytest
from ddt import ddt, data, unpack


@pytest.mark.usefixtures("one_time_setup", "set_up")
@ddt
class RegisterCoursesTests(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def classSetup(self, one_time_setup):
        self.login_page = LoginPage(self.driver)
        self.register_page = RegisterCoursesPage(self.driver)
        self.ts = TestStatus(self.driver)

    @pytest.mark.order(1)
    @data(("JavaScript", "JavaScript for beginners"),
          ("Test Automation", "Complete Test Automation Bundle"))
    @unpack
    def test_invalid_enrollment(self, search_param, course_name):
        # Navigating to the 'All Courses' page and searching for the course
        self.register_page.wait_for_courses_page_to_load()
        self.register_page.click_on_all_courses()
        self.register_page.search_course(course_name=search_param)
        self.register_page.click_on_course_to_enroll(course_name)

        # Click on Enroll on Course
        self.register_page.enroll_on_course()
        self.register_page.scroll_browser(direction="down")
        self.register_page.click_on_buy_button()

        is_error_banner = self.register_page.verify_cc_failed()

        self.ts.mark_final(test_name="test_invalid_enrollment",
                           result=is_error_banner,
                           result_message="CC information was incorrect")
