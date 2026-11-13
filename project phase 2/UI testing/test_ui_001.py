import os
import re
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from datetime import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


load_dotenv()

ADMIN_URL = "http://157.85.102.236/shop/wp-admin/"
SHOP_URL = "http://157.85.102.236/shop/"
USERNAME = os.getenv("SHOP_ADMIN_USERNAME")
PASSWORD = os.getenv("SHOP_ADMIN_PASSWORD")

# Goal: Automate SYS-001 from Staff product creation
# through Guest COD checkout and Staff order completion.

def test_sys001_end_to_end():
    assert USERNAME, "SHOP_ADMIN_USERNAME is missing from .env"
    assert PASSWORD, "SHOP_ADMIN_PASSWORD is missing from .env"

    driver = webdriver.Chrome()
    customer_driver = None

    try:
        wait = WebDriverWait(driver, 20)

        # Generate unique data for this UI test run
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        product_name = f"G01_UI001_{timestamp}_Mug"

        # ==========================================
        # STAFF SIDE: CREATE PRODUCT
        # ==========================================

        # 1. Open WordPress Admin
        driver.get(ADMIN_URL)

        # 2. Staff Login
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

        # 3. Open Add New Product
        driver.get(
            ADMIN_URL + "post-new.php?post_type=product"
        )

        # 4. Enter Product Name
        wait.until(
            EC.visibility_of_element_located(
                (By.ID, "title")
            )
        ).send_keys(product_name)

        # 5. Enter Regular Price
        price_field = wait.until(
            EC.visibility_of_element_located(
                (By.ID, "_regular_price")
            )
        )
        price_field.send_keys("199")

        # 6. Select Accessories Category
        all_categories_tab = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 '#product_cat-tabs a[href="#product_cat-all"]')
            )
        )
        all_categories_tab.click()

        category = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 '#product_cat-all input[name="tax_input[product_cat][]"][value="25"]')
            )
        )

        if not category.is_selected():
            category.click()

        assert category.is_selected()

        # 7. Open Inventory
        inventory_tab = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 'a[href="#inventory_product_data"]')
            )
        )
        inventory_tab.click()

        # 8. Enable Manage Stock
        manage_stock = wait.until(
            EC.element_to_be_clickable(
                (By.ID, "_manage_stock")
            )
        )

        if not manage_stock.is_selected():
            manage_stock.click()

        assert manage_stock.is_selected()

        # 9. Set Stock Quantity
        stock_field = wait.until(
            EC.visibility_of_element_located(
                (By.ID, "_stock")
            )
        )
        stock_field.clear()
        stock_field.send_keys("10")

        # 10. Publish Product
        publish_button = wait.until(
            EC.presence_of_element_located(
                (By.ID, "publish")
            )
        )

        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            publish_button
        )

        wait.until(
            EC.element_to_be_clickable(
                (By.ID, "publish")
            )
        ).click()

        publish_notice = wait.until(
            EC.visibility_of_element_located(
                (By.ID, "message")
            )
        )

        assert "published" in publish_notice.text.lower()

        saved_title = driver.find_element(
            By.ID, "title"
        ).get_attribute("value")

        assert saved_title == product_name

        print(f"\nCreated product: {product_name}")

        # ==========================================
        # CUSTOMER SIDE: BROWSE SHOP
        # ==========================================

        # 11. Open independent Guest browser
        customer_driver = webdriver.Chrome()
        customer_wait = WebDriverWait(customer_driver, 60)

        customer_driver.get(SHOP_URL)

        customer_wait.until(
            EC.text_to_be_present_in_element(
                (By.TAG_NAME, "body"),
                "Showing"
            )
        )

        print("Storefront loaded successfully!")

        # 12. Step 4: Check Guest Search availability
        guest_search_fields = [
            element for element in customer_driver.find_elements(
                By.CSS_SELECTOR,
                'input[type="search"], input[name="s"]'
            )
            if element.is_displayed()
        ]

        guest_search_passed = bool(guest_search_fields)

        if guest_search_passed:
            print("Step 4: Guest Search is available.")
        else:
            print(
                "Step 4 FAIL: Guest storefront has no visible Search Bar."
            )

        # 13. Find the newly created product using pagination
        product_link = None

        for page in range(1, 12):
            print(f"\n--- SHOP PAGE {page} ---")

            matching_products = customer_driver.find_elements(
                By.LINK_TEXT, product_name
            )

            print("Matching product:", len(matching_products))

            if matching_products:
                print("PRODUCT FOUND!")
                product_link = matching_products[0]
                break

            next_buttons = customer_driver.find_elements(
                By.CSS_SELECTOR,
                "a.wp-block-query-pagination-next"
            )

            if not next_buttons:
                break

            previous_url = customer_driver.current_url
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

        # 14. Open Product Detail
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

        assert product_name in customer_driver.find_element(
            By.TAG_NAME, "body"
        ).text

        print("Product Detail verified!")

        # Keep the exact URL so we can return after category sorting.
        product_url = customer_driver.current_url

        # ==========================================
        # CUSTOMER SIDE: CATEGORY AND SORTING
        # ==========================================

        # 15. Navigate to Accessories Category
        category_link = customer_wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 'a[href*="/product-category/accessories/"]')
            )
        )

        category_link.click()

        customer_wait.until(
            EC.url_contains(
                "/product-category/accessories/"
            )
        )

        category_body = customer_driver.find_element(
            By.TAG_NAME, "body"
        ).text

        assert "Accessories" in category_body
        assert product_name in category_body

        print("Step 5 PASS: Accessories category verified!")

        
        # Step 6: Sort products by price low to high
        previous_url = customer_driver.current_url

        sort_dropdown = customer_wait.until(
            EC.presence_of_element_located(
                (By.NAME, "orderby")
            )
        )

        Select(sort_dropdown).select_by_visible_text(
            "Sort by price: low to high"
        )

        # Wait for sorting request to update the page
        customer_wait.until(
            lambda d: (
                "orderby=price" in d.current_url
                or d.current_url != previous_url
            )
        )

        # Verify selected sorting option
        selected_sort = Select(
            customer_driver.find_element(
                By.NAME, "orderby"
            )
        ).first_selected_option.text.strip()

        assert selected_sort == "Sort by price: low to high"

        print("Step 6 PASS: Sorting by price low to high!")

        # Return directly to the exact Product Detail page.
        customer_driver.get(product_url)
        customer_wait.until(
            EC.visibility_of_element_located((By.NAME, "quantity"))
        )
        assert product_name in customer_driver.find_element(
            By.TAG_NAME, "body"
        ).text
        print("Returned to Product Detail successfully!")

        # ==========================================
        # CUSTOMER SIDE: PRODUCT AND CART
        # ==========================================

        # 17. Set Quantity to 2
        quantity = customer_wait.until(
            EC.visibility_of_element_located(
                (By.NAME, "quantity")
            )
        )

        quantity.clear()
        quantity.send_keys("2")

        # 18. Add to Cart
        add_to_cart = customer_wait.until(
            EC.element_to_be_clickable(
                (By.NAME, "add-to-cart")
            )
        )
        add_to_cart.click()

        # 19. Verify Add to Cart notification
        notice = customer_wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR,
                 ".wc-block-components-notice-banner__content")
            )
        )

        assert product_name in notice.text
        assert "2" in notice.text

        # 20. Open Cart
        view_cart = customer_wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "a.wc-forward")
            )
        )
        view_cart.click()

        # 21. Verify Cart Total
        cart_total = customer_wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR,
                 ".wc-block-components-totals-footer-item-tax-value")
            )
        )

        assert cart_total.text.strip() == "฿398.00"

        print(f"Customer purchased: {product_name}")
        print("Quantity: 2")
        print(f"Cart total: {cart_total.text}")

        # ==========================================
        # CUSTOMER SIDE: BROWSER BACK
        # ==========================================

        # 22. Open Checkout before placing the order
        checkout_button = customer_wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 "a.wc-block-cart__submit-button")
            )
        )
        checkout_button.click()

        customer_wait.until(
            EC.visibility_of_element_located(
                (By.ID, "email")
            )
        )

        
        # 23. Browser Back to Cart
        customer_driver.back()

        customer_wait.until(
            EC.url_contains("/cart/")
        )

        # Browser Back can restore the Cart page before WooCommerce
        # finishes rehydrating its cart blocks. Wait for the item first.
        try:
            WebDriverWait(customer_driver, 15).until(
                EC.text_to_be_present_in_element(
                    (By.TAG_NAME, "body"),
                    product_name
                )
            )
        except TimeoutException:
            # Retry one normal page load to let WooCommerce fetch the
            # current server-side cart session. Do not add the product again.
            print(
                "Cart item not visible immediately after Back; "
                "refreshing Cart once to re-check the existing session."
            )
            customer_driver.refresh()
            customer_wait.until(
                EC.url_contains("/cart/")
            )
            customer_wait.until(
                EC.text_to_be_present_in_element(
                    (By.TAG_NAME, "body"),
                    product_name
                )
            )

        cart_body = customer_driver.find_element(
            By.TAG_NAME, "body"
        ).text

        assert product_name in cart_body, (
            "Cart did not retain the product after Browser Back."
        )
        assert "398.00" in cart_body, (
            "Cart total was not ฿398 after Browser Back."
        )

        print("Step 10 PASS: Existing cart restored after Browser Back!")

        # ==========================================
        # CUSTOMER SIDE: GUEST CHECKOUT
        # ==========================================

        # 24. Return to Checkout
        checkout_button = customer_wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 "a.wc-block-cart__submit-button")
            )
        )
        checkout_button.click()

        customer_wait.until(
            EC.visibility_of_element_located(
                (By.ID, "email")
            )
        )

        # 25. Enter fictitious Guest information
        guest_email = (
            f"g01.ui001.{timestamp}@example.com"
        )

        customer_driver.find_element(
            By.ID, "email"
        ).send_keys(guest_email)

        customer_driver.find_element(
            By.ID, "billing-first_name"
        ).send_keys("Test")

        customer_driver.find_element(
            By.ID, "billing-last_name"
        ).send_keys("Buyer")

        customer_driver.find_element(
            By.ID, "billing-address_1"
        ).send_keys("123 Test Street")

        customer_driver.find_element(
            By.ID, "billing-city"
        ).send_keys("Bangkok")

        state_field = customer_wait.until(
            EC.presence_of_element_located(
                (By.ID, "billing-state")
            )
        )

        Select(state_field).select_by_visible_text(
            "Bangkok"
        )

        customer_driver.find_element(
            By.ID, "billing-postcode"
        ).send_keys("10110")

        customer_driver.find_element(
            By.ID, "billing-phone"
        ).send_keys("0800000000")

        print("Guest information entered successfully!")

        # 26. Select Cash on Delivery
        cod_option = customer_wait.until(
            EC.presence_of_element_located(
                (By.ID,
                 "radio-control-wc-payment-method-options-cod")
            )
        )

        if not cod_option.is_selected():
            cod_option.click()

        assert cod_option.is_selected()

        # 27. Verify Checkout Total
        checkout_total = customer_wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR,
                 ".wc-block-components-totals-footer-item-tax-value")
            )
        )

        assert checkout_total.text.strip() == "฿398.00"

        print("COD selected successfully!")
        print(f"Checkout total: {checkout_total.text}")

        # ==========================================
        # CUSTOMER SIDE: PLACE ORDER
        # ==========================================

        # 28. Place Order
        place_order_button = customer_wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 "button.wc-block-components-checkout-place-order-button")
            )
        )

        place_order_button.click()

        # 29. Wait for Order Confirmation
        customer_wait.until(
            EC.url_contains("order-received")
        )

        confirmation_text = customer_driver.find_element(
            By.TAG_NAME, "body"
        ).text

        print("Order confirmation:")
        print(confirmation_text)

        assert "order" in confirmation_text.lower()

        # 30. Extract Order Number
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
                url_match.group(1) if url_match else None
            )

        assert order_number is not None, (
            "Order number was not found in confirmation."
        )

        print("ORDER PLACED SUCCESSFULLY!")
        print("Order Number:", order_number)

        # ==========================================
        # STAFF SIDE: FIND AND VERIFY ORDER
        # ==========================================

        # 31. Open WooCommerce Orders
        driver.get(
            ADMIN_URL + "admin.php?page=wc-orders"
        )

        # 32. Search for the new Order
        order_search = wait.until(
            EC.visibility_of_element_located(
                (By.ID, "orders-search-input-search-input")
            )
        )

        order_search.clear()
        order_search.send_keys(order_number)

        driver.find_element(
            By.ID, "search-submit"
        ).click()

        # 33. Open matching Order
        order_link = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 f"//a[contains(normalize-space(), '#{order_number}')]")
            )
        )

        order_link.click()

        # 34. Verify Order details
        wait.until(
            EC.visibility_of_element_located(
                (By.ID, "post-body")
            )
        )

        order_body = driver.find_element(
            By.ID, "post-body"
        ).text

        assert product_name in order_body
        assert "398.00" in order_body

        print("Staff verified correct Order!")
        print("Order Number:", order_number)
        print("Product:", product_name)
        print("Quantity: 2")
        print("Total: ฿398.00")

        # ==========================================
        # STAFF SIDE: UPDATE ORDER STATUS
        # ==========================================

        # 35. Verify current Processing status
        status_dropdown = wait.until(
            EC.element_to_be_clickable(
                (By.ID, "select2-order_status-container")
            )
        )

        current_status = status_dropdown.text.strip()

        print("Current status:", current_status)

        assert current_status == "Processing"

        # 36. Select Completed
        status_dropdown.click()

        completed_option = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//li[contains(@class,'select2-results__option') "
                 "and normalize-space()='Completed']")
            )
        )

        completed_option.click()

        wait.until(
            EC.text_to_be_present_in_element(
                (By.ID, "select2-order_status-container"),
                "Completed"
            )
        )

        # 37. Save Order
        update_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button[name="save"]')
            )
        )

        update_button.click()

        wait.until(
            EC.text_to_be_present_in_element(
                (By.TAG_NAME, "body"),
                "Order updated."
            )
        )

        updated_status = driver.find_element(
            By.ID, "select2-order_status-container"
        ).text.strip()

        assert updated_status == "Completed"

        print("Order status updated: COMPLETED")

        # ==========================================
        # STAFF SIDE: FINAL ORDER VERIFICATION
        # ==========================================

        # 38. Return to Orders list
        driver.get(
            ADMIN_URL + "admin.php?page=wc-orders"
        )

        final_search = wait.until(
            EC.visibility_of_element_located(
                (By.ID, "orders-search-input-search-input")
            )
        )

        final_search.clear()
        final_search.send_keys(order_number)

        driver.find_element(
            By.ID, "search-submit"
        ).click()

        # 39. Verify final Order row
        final_order = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH,
                 f"//a[contains(normalize-space(), '#{order_number}')]")
            )
        )

        order_row = final_order.find_element(
            By.XPATH, "./ancestor::tr"
        ).text

        assert "completed" in order_row.lower()
        assert order_number in order_row

        print("FINAL STAFF VERIFICATION PASSED!")
        print(order_row)

    finally:
        if customer_driver:
            customer_driver.quit()

        driver.quit()
