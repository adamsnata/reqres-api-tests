import os

import allure
from allure_commons.types import Severity
from faker import Faker
from allure_commons._allure import step
from selene import have
from selene.support.conditions import be
from selene.support.shared import browser

fake = Faker()

@allure.label('owner', 'Maxim Veselov')
@allure.feature('Web')
@allure.severity(Severity.NORMAL)
@allure.story('demowebshop')
def test_check_cart_quantity(demoshop, app, clean_cart):
    app.open("")
    demoshop.add_computing_and_internet_book_to_cart(count=4)
    demoshop.add_book_fiction_to_cart(count=3)
    demoshop.add_health_book_to_cart(count=2)
    app.element('.ico-cart .cart-label').click()
    with step('check cart size'):
        app.element('.cart-label~.cart-qty').should(have.text('(9)'))

@allure.label('owner', 'Maxim Veselov')
@allure.feature('Web')
@allure.severity(Severity.NORMAL)
@allure.story('demowebshop')
def test_gift_cards_match(demoshop, app, clean_cart):
    app.open('https://demowebshop.tricentis.com/gift-cards')
    recipient_info = {
        "name": fake.first_name(),
        "email": fake.email()
    }

    def fill_recipient_info():
        app.element('.recipient-name').type(recipient_info["name"])
        app.element(".recipient-email").type(recipient_info["email"])
        app.element('[id|=add-to-cart-button][type="button"]').click()

    app.element('.product-title>[href="/25-virtual-gift-card"]').click()
    fill_recipient_info()
    response = demoshop.demoqa.get('/cart')
    with step('Check recipient info'):
        assert recipient_info['name'], recipient_info['email'] in response.text
        app.element('.ico-cart .cart-label').click()


@allure.label('owner', 'Maxim Veselov')
@allure.feature('Web')
@allure.severity(Severity.NORMAL)
@allure.story('demowebshop')
def test_books_match(demoshop, app, clean_cart):
    app.open('https://demowebshop.tricentis.com/books')
    for book in browser.elements('[type = "button"][value = "Add to cart"]'):
        book.click()
        browser.wait_until(book.should(be.clickable))
    response = demoshop.demoqa.get('/cart')
    with step('check total price'):
        assert '44.00' in response.text


@allure.label('owner', 'Maxim Veselov')
@allure.feature('Web')
@allure.severity(Severity.NORMAL)
@allure.story('demowebshop')
def test_add_digital_downloads_to_wishlist(demoshop, app, clean_wishlist):
    app.open("")
    demoshop.add_3rd_album_to_wishlist()
    demoshop.add_music2_blue_to_wishlist()
    demoshop.add_music2_yellow_to_wishlist()
    app.element('#topcartlink~li .ico-wishlist').click()
    with step('check wishlist content'):
        app.element('.share-link').should(be.existing).click()
        app.all('.product>[href]').should(have.texts('3rd Album', 'Music 2', 'Music 2'))


@allure.label('owner', 'Maxim Veselov')
@allure.feature('Web')
@allure.severity(Severity.NORMAL)
@allure.feature('Web')
@allure.story('demowebshop')
def test_compare_desktop_pc(app, clear_compare_list):
    app.open('https://demowebshop.tricentis.com/desktops')
    app.element('.product-title>[href="/build-your-cheap-own-computer"]').click()
    app.element('[type="radio"][value="65"]').click()
    app.element('[type="radio"][value="55"]').click()
    app.element('[type="radio"][value="58"]').click()
    app.element('[type="checkbox"][value="94"]').click()
    app.element('[type = "button"][value="Add to compare list"]').click()
    app.open('https://demowebshop.tricentis.com/notebooks')
    app.element('.product-title>[href="/141-inch-laptop"]').click()
    app.element('[type = "button"][value="Add to compare list"]').click()
    app.save_screenshot('compare.png')
    with step('check screenshot not empty'):
        assert os.path.getsize('compare.png') != 0
    os.remove('compare.png')














    













