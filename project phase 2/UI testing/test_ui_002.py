import os
import re

from datetime import datetime
from dotenv import load_dotenv
from selenium.common.exceptions import StaleElementReferenceException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


load_dotenv()

ADMIN_URL = "http://157.85.102.236/shop/wp-admin/"
SHOP_URL = "http://157.85.102.236/shop/"

USERNAME = os.getenv("SHOP_ADMIN_USERNAME")
PASSWORD = os.getenv("SHOP_ADMIN_PASSWORD")


# Goal:
# Automate SYS-002:
# Staff creates a product and a 10% coupon.
# Guest customer verifies invalid coupon rejection,
# applies the valid coupon, checks the discount,
# and completes COD checkout.

def test_sys002_end_to_end():

    assert USERNAME, "SHOP_ADMIN_USERNAME is missing from .env"
    assert PASSWORD, "SHOP_ADMIN_PASSWORD is missing from .env"

    driver = webdriver.Chrome()
    customer_driver = None

    try:
        # Shared classroom server can respond slowly.
        wait = WebDriverWait(driver, 60)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        product_name = f"G01_UI002_{timestamp}_Tee"
        coupon_code = f"G01UI002{timestamp}"
        invalid_coupon = f"INVALID{timestamp}"

        # ==========================================
        # STAFF SIDE: LOGIN
        # ==========================================

        driver.get(ADMIN_URL)

        wait.until(
            EC.visibility_of_element_located(
                (By.ID, "user_login")
            )
        ).send_keys(USERNAME)

        driver.find_element(
            By.ID, "user_pass"
        ).send_keys(PASSWORD)

        driver.find_element(
            By.ID, "wp-submit"
        ).click()

        wait.until(
            EC.visibility_of_element_located(
                (By.ID, "dashboard-widgets-wrap")
            )
        )

        print("Staff login successful!")

        # ==========================================
        # STAFF SIDE: CREATE PRODUCT
        # ==========================================

        driver.get(
            ADMIN_URL + "post-new.php?post_type=product"
        )

        # Product name
        wait.until(
            EC.visibility_of_element_located(
                (By.ID, "title")
            )
        ).send_keys(product_name)

        # Regular price = 200. Trigger blur/change so WooCommerce saves it.
        price_field = wait.until(
            EC.visibility_of_element_located(
                (By.ID, "_regular_price")
            )
        )
        price_field.clear()
        price_field.send_keys("200")
        price_field.send_keys(Keys.TAB)

        # Verify the value is present before publishing.
        wait.until(
            lambda d: d.find_element(
                By.ID, "_regular_price"
            ).get_attribute("value") == "200"
        )
        entered_price = driver.find_element(
            By.ID, "_regular_price"
        ).get_attribute("value")
        print("Product price entered:", entered_price)
        assert entered_price == "200"

        # Select Accessories using the exact checkbox value confirmed in DevTools.
        all_categories_tab = wait.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    '#product_cat-tabs a[href="#product_cat-all"]'
                )
            )
        )
        all_categories_tab.click()

        category = wait.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    '#product_cat-all input[name="tax_input[product_cat][]"][value="25"]'
                )
            )
        )
        if not category.is_selected():
            category.click()

        # Confirm the checkbox state before saving.
        wait.until(
            lambda d: d.find_element(
                By.CSS_SELECTOR,
                '#product_cat-all input[name="tax_input[product_cat][]"][value="25"]'
            ).is_selected()
        )
        category = driver.find_element(
            By.CSS_SELECTOR,
            '#product_cat-all input[name="tax_input[product_cat][]"][value="25"]'
        )
        print("Accessories selected:", category.is_selected())
        assert category.is_selected()

        # Publish Product
        publish_button = wait.until(
            EC.element_to_be_clickable((By.ID, "publish"))
        )
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            publish_button
        )
        publish_button.click()

        # Wait for WordPress to leave the new-post screen.
        wait.until(
            lambda d: (
                "post.php" in d.current_url
                and "post-new.php" not in d.current_url
            )
        )

        # Verify the saved title and price on the edit page.
        saved_product_name = wait.until(
            EC.presence_of_element_located((By.ID, "title"))
        ).get_attribute("value")
        assert saved_product_name == product_name

        saved_price = wait.until(
            EC.presence_of_element_located((By.ID, "_regular_price"))
        ).get_attribute("value")
        print("Saved product price:", saved_price)
        assert saved_price == "200", (
            f"Product price was not saved. Found: {saved_price!r}"
        )

        # Verify Accessories remained selected after saving.
        saved_category = wait.until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    '#product_cat-all input[name="tax_input[product_cat][]"][value="25"]'
                )
            )
        )
        print("Saved Accessories category:", saved_category.is_selected())
        assert saved_category.is_selected(), (
            "Accessories category was not saved."
        )

        # Verify WordPress stored the product as Published, not Draft.
        post_status = driver.execute_script(
            "return document.querySelector('#post_status')?.value || '';"
        )
        print("Saved product status:", post_status)
        assert post_status == "publish", (
            f"Product was not published. Current status: {post_status!r}"
        )

        print(f"\nCreated product: {product_name}")
        print("Product price: ฿200.00")
        print("Accessories category verified!")
        print("Product published successfully!")

        # ==========================================
        # STAFF SIDE: CREATE 10% COUPON
        # ==========================================

        driver.get(
            ADMIN_URL + "post-new.php?post_type=shop_coupon"
        )

        # Coupon code
        coupon_title = wait.until(
            EC.visibility_of_element_located(
                (By.ID, "title")
            )
        )

        coupon_title.send_keys(coupon_code)

        # Discount type = Percentage discount
        discount_type = wait.until(
            EC.presence_of_element_located(
                (By.ID, "discount_type")
            )
        )

        Select(
            discount_type
        ).select_by_visible_text(
            "Percentage discount"
        )

        # Coupon amount = 10%
        coupon_amount = wait.until(
            EC.visibility_of_element_located(
                (By.ID, "coupon_amount")
            )
        )

        coupon_amount.clear()
        coupon_amount.send_keys("10")

        # Publish Coupon
        coupon_publish = wait.until(
            EC.presence_of_element_located(
                (By.ID, "publish")
            )
        )

        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            coupon_publish
        )

        coupon_publish = wait.until(
            EC.element_to_be_clickable(
                (By.ID, "publish")
            )
        )

        coupon_publish.click()

        # Wait up to 60 seconds for WooCommerce
        # to confirm that the coupon was saved.
        
                # Wait until WordPress finishes publishing the coupon
        wait.until(
            lambda d: (
                "post.php" in d.current_url
                and "post-new.php" not in d.current_url
            )
        )

        # Verify the saved coupon code
        saved_coupon = wait.until(
            EC.presence_of_element_located(
                (By.ID, "title")
            )
        ).get_attribute("value")

        assert saved_coupon == coupon_code
        # Verify saved coupon settings
        saved_discount_type = Select(
            driver.find_element(
                By.ID, "discount_type"
            )
        ).first_selected_option.text.strip()

        saved_amount = driver.find_element(
            By.ID, "coupon_amount"
        ).get_attribute("value")

        assert saved_discount_type == "Percentage discount"
        assert saved_amount in ("10", "10.00")

        print(f"Created coupon: {coupon_code}")
        print("Coupon discount: 10%")
        print("Coupon published successfully!")

        # ==========================================
        # CUSTOMER SIDE: OPEN GUEST STOREFRONT
        # ==========================================

        customer_driver = webdriver.Chrome()

        # Same long wait strategy used successfully in SYS-001
        customer_wait = WebDriverWait(
            customer_driver,
            60
        )

        customer_driver.get(SHOP_URL)

        customer_wait.until(
            EC.text_to_be_present_in_element(
                (By.TAG_NAME, "body"),
                "Showing"
            )
        )

        print("Storefront loaded successfully!")

        # ==========================================
        # CUSTOMER SIDE: FIND NEW PRODUCT
        # ==========================================

        product_link = None

        # More pages than SYS-001 in case the shared
        # server receives additional products.
        for page in range(1, 20):

            print(f"\n--- SHOP PAGE {page} ---")

            matching_products = (
                customer_driver.find_elements(
                    By.LINK_TEXT,
                    product_name
                )
            )

            print(
                "Matching product:",
                len(matching_products)
            )

            if matching_products:
                product_link = matching_products[0]
                print("PRODUCT FOUND!")
                break

            next_buttons = (
                customer_driver.find_elements(
                    By.CSS_SELECTOR,
                    "a.wp-block-query-pagination-next"
                )
            )

            if not next_buttons:
                print("No more Shop pages.")
                break

            previous_url = (
                customer_driver.current_url
            )

            next_buttons[0].click()

            customer_wait.until(
                EC.url_changes(previous_url)
            )

            customer_wait.until(
                EC.text_to_be_present_in_element(
                    (By.TAG_NAME, "body"),
                    "Showing"
                )
            )

        assert product_link is not None, (
            f"Product not found: {product_name}"
        )

        # Re-find before clicking to avoid stale element
        product_link = customer_wait.until(
            EC.element_to_be_clickable(
                (By.LINK_TEXT, product_name)
            )
        )

        product_link.click()

        customer_wait.until(
            EC.visibility_of_element_located(
                (By.NAME, "quantity")
            )
        )

        product_body = customer_driver.find_element(
            By.TAG_NAME, "body"
        ).text

        assert product_name in product_body

        print("Product Detail verified!")

        # ==========================================
        # CUSTOMER SIDE: ADD 2 TO CART
        # ==========================================

        quantity = customer_wait.until(
            EC.visibility_of_element_located(
                (By.NAME, "quantity")
            )
        )

        quantity.clear()
        quantity.send_keys("2")

        add_to_cart = customer_wait.until(
            EC.element_to_be_clickable(
                (By.NAME, "add-to-cart")
            )
        )

        add_to_cart.click()

        notice = customer_wait.until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    ".wc-block-components-notice-banner__content"
                )
            )
        )

        assert product_name in notice.text
        assert "2" in notice.text

        print("Product added to cart!")
        print("Quantity: 2")

        # ==========================================
        # CUSTOMER SIDE: OPEN CART
        # ==========================================

        view_cart = customer_wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "a.wc-forward")
            )
        )

        view_cart.click()

        # Wait for this exact product to appear
        customer_wait.until(
            EC.text_to_be_present_in_element(
                (By.TAG_NAME, "body"),
                product_name
            )
        )

        cart_body = customer_driver.find_element(
            By.TAG_NAME, "body"
        ).text

        assert product_name in cart_body
        assert "400.00" in cart_body

        print("Cart verified!")
        print("Subtotal before coupon: ฿400.00")

        # ==========================================
        # CUSTOMER SIDE: INVALID COUPON
        # ==========================================

        # Open Add coupons panel
        add_coupon_panel = customer_wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//*[normalize-space()='Add coupons']"
                )
            )
        )

        add_coupon_panel.click()

        # Coupon input
        coupon_input = customer_wait.until(
            EC.visibility_of_element_located(
                (
                    By.ID,
                    "wc-block-components-totals-coupon__input-coupon"
                )
            )
        )

        coupon_input.clear()
        coupon_input.send_keys(invalid_coupon)

        coupon_form = customer_driver.find_element(
            By.ID,
            "wc-block-components-totals-coupon__form"
        )

        invalid_apply_button = (
            coupon_form.find_element(
                By.CSS_SELECTOR,
                'button[type="submit"]'
            )
        )

        invalid_apply_button.click()

        # Wait up to 60 seconds for rejection message
        invalid_error = customer_wait.until(
            EC.visibility_of_element_located(
                (By.ID, "validate-error-coupon")
            )
        )

        invalid_error_text = (
            invalid_error.text.lower()
        )

        assert (
            "does not exist" in invalid_error_text
            or "cannot be applied" in invalid_error_text
        )

        # Invalid coupon must not change the total
        invalid_cart_body = (
            customer_driver.find_element(
                By.TAG_NAME, "body"
            ).text
        )

        assert "400.00" in invalid_cart_body

        print("Invalid coupon rejected successfully!")
        print("Total remains: ฿400.00")

        # ==========================================
        # CUSTOMER SIDE: VALID COUPON
        # ==========================================

        # Re-locate the input after the invalid-coupon response.
        coupon_input = customer_wait.until(
            EC.element_to_be_clickable(
                (
                    By.ID,
                    "wc-block-components-totals-coupon__input-coupon"
                )
            )
        )

        # Replace the invalid code completely.
        coupon_input.click()
        coupon_input.send_keys(Keys.CONTROL, "a")
        coupon_input.send_keys(Keys.BACKSPACE)
        coupon_input.send_keys(coupon_code)

        entered_coupon = coupon_input.get_attribute("value")
        print("Coupon expected:", coupon_code)
        print("Coupon entered:", entered_coupon)
        assert entered_coupon == coupon_code

        coupon_form = customer_driver.find_element(
            By.ID,
            "wc-block-components-totals-coupon__form"
        )

        valid_apply_button = coupon_form.find_element(
            By.CSS_SELECTOR,
            'button[type="submit"]'
        )

        valid_apply_button.click()

        # Wait for the actual expected result: discounted total.
        customer_wait.until(
            EC.text_to_be_present_in_element(
                (By.TAG_NAME, "body"),
                "360.00"
            )
        )

        discounted_cart = customer_driver.find_element(
            By.TAG_NAME, "body"
        ).text

        assert "40.00" in discounted_cart
        assert "360.00" in discounted_cart

        print("Valid coupon applied successfully!")
        print("Discount: -฿40.00")
        print("Final total: ฿360.00")

        # ==========================================
        # CUSTOMER SIDE: CHECKOUT
        # ==========================================

        checkout_button = customer_wait.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "a.wc-block-cart__submit-button"
                )
            )
        )

        checkout_button.click()

        # Wait up to 60 seconds for checkout
        customer_wait.until(
            EC.visibility_of_element_located(
                (By.ID, "email")
            )
        )

        # ==========================================
        # CUSTOMER SIDE: GUEST INFORMATION
        # ==========================================

        guest_email = (
            f"g01.ui002.{timestamp}@example.com"
        )

        email_field = customer_wait.until(
            EC.visibility_of_element_located(
                (By.ID, "email")
            )
        )

        email_field.clear()
        email_field.send_keys(guest_email)

        first_name = customer_driver.find_element(
            By.ID, "billing-first_name"
        )
        first_name.clear()
        first_name.send_keys("Test")

        last_name = customer_driver.find_element(
            By.ID, "billing-last_name"
        )
        last_name.clear()
        last_name.send_keys("Buyer")

        address = customer_driver.find_element(
            By.ID, "billing-address_1"
        )
        address.clear()
        address.send_keys("123 Test Street")

        city = customer_driver.find_element(
            By.ID, "billing-city"
        )
        city.clear()
        city.send_keys("Bangkok")

        state_field = customer_wait.until(
            EC.presence_of_element_located(
                (By.ID, "billing-state")
            )
        )

        Select(
            state_field
        ).select_by_visible_text(
            "Bangkok"
        )

        postcode = customer_driver.find_element(
            By.ID, "billing-postcode"
        )
        postcode.clear()
        postcode.send_keys("10110")

        phone = customer_driver.find_element(
            By.ID, "billing-phone"
        )
        phone.clear()
        phone.send_keys("0800000000")

        print("Guest information entered successfully!")

        # ==========================================
        # CUSTOMER SIDE: CASH ON DELIVERY
        # ==========================================

        cod_option = customer_wait.until(
            EC.presence_of_element_located(
                (
                    By.ID,
                    "radio-control-wc-payment-method-options-cod"
                )
            )
        )

        if not cod_option.is_selected():
            cod_option.click()

        assert cod_option.is_selected()

        # Wait until checkout reflects final total
        customer_wait.until(
            EC.text_to_be_present_in_element(
                (By.TAG_NAME, "body"),
                "360.00"
            )
        )

        checkout_body = customer_driver.find_element(
            By.TAG_NAME, "body"
        ).text

        assert product_name in checkout_body
        assert "360.00" in checkout_body

        print("COD selected successfully!")
        print("Checkout total: ฿360.00")

        # ==========================================
        # CUSTOMER SIDE: PLACE ORDER
        # ==========================================

        place_order_button = customer_wait.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "button.wc-block-components-checkout-place-order-button"
                )
            )
        )

        driver_before_order_url = (
            customer_driver.current_url
        )

        place_order_button.click()

        # Shared server may take time to create order.
        # Wait up to 60 seconds for confirmation URL.
        customer_wait.until(
            EC.url_contains("order-received")
        )

        assert (
            customer_driver.current_url
            != driver_before_order_url
        )

        confirmation_text = (
            customer_driver.find_element(
                By.TAG_NAME, "body"
            ).text
        )

        assert product_name in confirmation_text
        assert "360.00" in confirmation_text

        print("\nOrder confirmation:")
        print(confirmation_text)

        # ==========================================
        # EXTRACT ORDER NUMBER
        # ==========================================

        order_match = re.search(
            r"Order\s*(?:number|#)\s*:?\s*#?(\d+)",
            confirmation_text,
            re.IGNORECASE
        )

        if order_match:
            order_number = order_match.group(1)

        else:
            url_match = re.search(
                r"order-received/(\d+)",
                customer_driver.current_url
            )

            order_number = (
                url_match.group(1)
                if url_match
                else None
            )

        assert order_number is not None, (
            "Order number was not found "
            "on the confirmation page."
        )

        print("\nSYS-002 CUSTOMER FLOW PASSED!")
        print("Product:", product_name)
        print("Quantity: 2")
        print("Subtotal: ฿400.00")
        print("Coupon:", coupon_code)
        print("Discount: -฿40.00")
        print("Final Total: ฿360.00")
        print("Payment: Cash on delivery")
        print("Order Number:", order_number)

        # ==========================================
        # STAFF SIDE: VERIFY THE NEW ORDER
        # ==========================================

        # Reuse the authenticated Staff browser and the Order Number
        # extracted from this run. Do not hardcode a previous Order ID.
        driver.get(ADMIN_URL + "admin.php?page=wc-orders")

        order_search = wait.until(
            EC.visibility_of_element_located(
                (By.ID, "orders-search-input-search-input")
            )
        )
        order_search.clear()
        order_search.send_keys(order_number)
        driver.find_element(By.ID, "search-submit").click()

        order_xpath = (
            f"//a[contains(normalize-space(), '#{order_number}')]"
        )

        def find_order_link(d):
            try:
                for link in d.find_elements(By.XPATH, order_xpath):
                    if link.is_displayed() and link.is_enabled():
                        return link
                return False
            except StaleElementReferenceException:
                return False

        wait.until(find_order_link)
        wait.until(
            EC.element_to_be_clickable((By.XPATH, order_xpath))
        ).click()

        wait.until(
            EC.visibility_of_element_located((By.ID, "post-body"))
        )

        order_body = driver.find_element(By.ID, "post-body").text
        assert product_name in order_body
        assert coupon_code.lower() in order_body.lower()
        assert "400.00" in order_body
        assert "40.00" in order_body
        assert "360.00" in order_body

        status = wait.until(
            EC.visibility_of_element_located(
                (By.ID, "select2-order_status-container")
            )
        ).text.strip()
        assert status == "Processing"

        print("\nSYS-002 STAFF VERIFICATION PASSED!")
        print("Order Number:", order_number)
        print("Product:", product_name)
        print("Quantity: 2")
        print("Coupon:", coupon_code)
        print("Subtotal: ฿400.00")
        print("Discount: -฿40.00")
        print("Total: ฿360.00")
        print("Status:", status)

    finally:
        if customer_driver:
            customer_driver.quit()

        driver.quit()
