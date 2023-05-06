import os

import pytest
from dotenv import load_dotenv
from selene.support.conditions import have, be
from selene.support.shared import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from framework.demoqa_with_env import DemoQaWithEnv
from utils import attach

load_dotenv()
authorization_cookie = None


def pytest_addoption(parser):
    parser.addoption("--env", default="prod")


@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")


@pytest.fixture(scope='session')
def demoshop(env):
    return DemoQaWithEnv(env)


@pytest.fixture(scope='session')
def reqres(env):
    return DemoQaWithEnv(env).reqres


@pytest.fixture(scope='function')
def app(demoshop):
    global authorization_cookie
    options = Options()
    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": "100.0",
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
    options.capabilities.update(selenoid_capabilities)
    login = os.getenv('LOGIN_SELENOID')
    password = os.getenv('PASSWORD_SELENOID')
    driver = webdriver.Remote(
        command_executor=f"https://{login}:{password}@selenoid.autotests.cloud/wd/hub",
        options=options)
    browser.config.driver = driver
    browser.config.base_url = (os.getenv("API_URL"))
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    if authorization_cookie is None:
        response = demoshop.login(
            os.getenv("LOGIN"), os.getenv("PASSWORD"))
        authorization_cookie = response.cookies.get("NOPCOMMERCE.AUTH")
    browser.open("Themes/DefaultClean/Content/images/logo.png")
    browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": authorization_cookie})
    yield browser
    attach.add_screenshot(browser)
    attach.add_video(browser)


@pytest.fixture(scope='function')
def clean_cart(app):
    app.open('https://demowebshop.tricentis.com/cart')
    yield app
    app.open('https://demowebshop.tricentis.com/cart')
    for checkbox in app.elements('[name="removefromcart"]'):
        checkbox.click()
    app.element('[name="updatecart"]').click()
    app.element('.order-summary-content').should(have.text('Your Shopping Cart is empty!'))


@pytest.fixture()
def clean_wishlist():
    yield app
    browser.open('https://demowebshop.tricentis.com/wishlist')
    for checkbox in browser.elements('[name="removefromcart"]'):
        checkbox.click()
    browser.element('[value="Update wishlist"]').click()
    browser.element('.wishlist-content').should(have.text('The wishlist is empty!'))


@pytest.fixture()
def clear_compare_list():
    yield app
    browser.element('.clear-list').click()
    browser.element('.page-body').should(have.text('You have no items to compare.'))
