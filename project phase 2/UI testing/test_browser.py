
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def test_open_woocommerce():
    options = Options()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)

    driver.get("http://157.85.102.236/shop/")

    assert "shop" in driver.current_url.lower()



from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_open_product():
    driver = webdriver.Chrome()

    try:
        driver.get("http://157.85.102.236/shop/")

        # Wait until the Album link appears
        album = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(
                (By.LINK_TEXT, "Album")
            )
        )

        # Click the product
        album.click()

        # Verify product detail page
        WebDriverWait(driver, 15).until(
            EC.url_contains("/product/album/")
        )

        assert "album" in driver.current_url.lower()

    finally:
        driver.quit()


def test_add_album_to_cart():
    driver = webdriver.Chrome()

    try:
        # Open shop
        driver.get("http://157.85.102.236/shop/")

        # Find and click Album
        album = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(
                (By.LINK_TEXT, "Album")
            )
        )
        album.click()

        # Find Add to cart button
        add_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.single_add_to_cart_button")
            )
        )

        # Click Add to cart
        add_button.click()

        # Open cart
        driver.get("http://157.85.102.236/shop/cart/")

        # Verify product appears in cart
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Album')]")
            )
        )

        assert "Album" in driver.find_element(
            By.TAG_NAME, "body"
        ).text

    finally:
        driver.quit()
