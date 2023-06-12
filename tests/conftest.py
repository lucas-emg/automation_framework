import pytest
from base.webdriverfactory import WebDriverFactory


@pytest.fixture()
def set_up():
    print("Running method level setup")
    yield
    print("Running method level teardown")


@pytest.fixture(scope="class")
def one_time_setup(browser, os_type, request):
    print("Running module level setup")
    wdf = WebDriverFactory(browser)
    driver = wdf.get_web_driver_instance()

    if request.cls is not None:
        request.cls.driver = driver

    yield driver
    driver.quit()
    print("Running module level teardown")


def pytest_addoption(parser):
    parser.addoption("--browser")
    parser.addoption("--os_type", help="Type of operating system")


@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def os_type(request):
    return request.config.getoption("--os_type")
