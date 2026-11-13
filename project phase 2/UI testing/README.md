# Automated UI Testing

**Course:** ITCS386 — Software Verification and Validation  
**Project:** Project Phase 2  
**Group:** G01  
**System Under Test:** WooCommerce Online Shop

---

## 1. Project Overview

This folder contains the Automated UI Testing implementation for the WooCommerce online shop.

The objective is to automate three system test scenarios using Selenium WebDriver, Python, and Pytest. Each automated UI test follows the corresponding system test scenario and checks the expected results through the website interface.

The tests cover end-to-end workflows involving staff and guest customers, including product management, product purchasing, coupon validation, inventory limits, cart operations, guest checkout, and staff order verification.

## 2. Testing Tools and Environment

| Tool | Purpose |
|---|---|
| Python 3.12 | Programming language |
| Pytest | Test execution framework |
| Selenium WebDriver | Browser automation |
| Google Chrome | Web browser |
| python-dotenv | Loading environment variables |
| WordPress / WooCommerce | System under test |

The tests use separate browser sessions for staff and guest customer activities. Staff credentials are loaded from a local `.env` file and are not hardcoded in the test scripts.

## 3. Automated End-to-End Test Scenarios

### 3.1 UI-001: Product Discovery, Purchase and Order Management

**Based on:** SYS-001  
**Test file:** `test_ui_001.py`

**Objective:** Verify that staff can create and publish a product, customers can find and purchase it, and staff can verify and manage the resulting order.

**Test Data**

| Item | Value |
|---|---|
| Product name | `G01_UI001_<timestamp>_Mug` |
| Product type | Simple Product |
| Product price | THB 199 |
| Category | Accessories |
| Purchase quantity | 2 |
| Expected subtotal | THB 398 |
| Customer type | Guest |
| Payment method | Cash on Delivery (COD) |

**End-to-End Test Flow**

| Step | Role | Action | Expected Result |
|---:|---|---|---|
| 1 | Staff | Log in to WordPress Admin | Login successful |
| 2 | Staff | Create a new product | Product created |
| 3 | Staff | Set product price and category | Price THB 199; Accessories selected |
| 4 | Staff | Publish the product | Product published |
| 5 | Customer (Guest) | Open storefront and find the product | Product found |
| 6 | Customer (Guest) | Open product details | Correct product displayed |
| 7 | Customer (Guest) | Add two items to cart | Quantity 2 |
| 8 | Customer (Guest) | Verify cart total | THB 398 |
| 9 | Customer (Guest) | Complete checkout using COD | Checkout successful |
| 10 | Customer (Guest) | Place the order | Order created |
| 11 | Staff | Search for the new order | Correct order found |
| 12 | Staff | Verify product, quantity, and total | Order details match |

**Observed limitation:** The guest storefront did not display a visible Search Bar during the test. Product discovery was completed using pagination instead. Search availability was not considered verified.

**Final execution result:** PASS  
**Recorded execution time:** 54.99 seconds

**Development issue:** The missing visible Search Bar was handled by using product listing pagination to locate the product. This is an observed storefront limitation, not a successful search test.

### 3.2 UI-002: Coupon Validation and Discount

**Based on:** SYS-002  
**Test file:** `test_ui_002.py`

**Objective:** Verify that invalid coupons are rejected and valid percentage coupons are applied correctly during checkout.

**Test Data**

| Item | Value |
|---|---:|
| Product price | THB 200 |
| Purchase quantity | 2 |
| Subtotal | THB 400 |
| Coupon type | Percentage discount |
| Coupon discount | 10% |
| Discount amount | THB 40 |
| Expected total | THB 360 |
| Customer type | Guest |
| Payment method | Cash on Delivery (COD) |

**End-to-End Test Flow**

| Step | Role | Action | Expected Result |
|---:|---|---|---|
| 1 | Staff | Log in | Login successful |
| 2 | Staff | Create a new product | Product created |
| 3 | Staff | Set product price and category | Price THB 200; Accessories selected |
| 4 | Staff | Publish the product | Product published |
| 5 | Staff | Create and publish a 10% coupon | Coupon created |
| 6 | Customer (Guest) | Find the new product | Product found |
| 7 | Customer (Guest) | Add two items to cart | Subtotal THB 400 |
| 8 | Customer (Guest) | Apply an invalid coupon | Coupon rejected; total unchanged |
| 9 | Customer (Guest) | Apply the valid coupon | 10% discount applied |
| 10 | Customer (Guest) | Verify discount and total | Discount THB 40; total THB 360 |
| 11 | Customer (Guest) | Complete checkout using COD | Checkout successful |
| 12 | Customer (Guest) | Place the order | Order created |
| 13 | Staff | Search for and open the order | Correct order found |
| 14 | Staff | Verify product, coupon, discount, and total | Order details match |

**Final execution result:** PASS  
**Recorded execution time:** 51.89 seconds

**Development issues:** Product publishing timeouts and stale element errors occurred during early executions. Explicit waits and re-finding dynamic page elements were used to address these automation issues. The final recorded end-to-end execution passed.

### 3.3 UI-003: Inventory Limits, Cart Changes and Guest Checkout

**Based on:** SYS-003  
**Test file:** `test_ui_003.py`

**Objective:** Verify stock-aware quantity validation, cart operations, guest checkout, and inventory updates after a successful purchase.

**Test Data**

| Item | Value |
|---|---:|
| Product price | THB 150 |
| Initial stock | 3 |
| Invalid quantity | 0 |
| Over-stock quantity | 4 |
| Valid purchase quantity | 2 |
| Expected order total | THB 300 |
| Expected remaining stock | 1 |
| Customer type | Guest |
| Payment method | Cash on Delivery (COD) |

**End-to-End Test Flow**

| Step | Role | Action | Expected Result |
|---:|---|---|---|
| 1 | Staff | Log in | Login successful |
| 2 | Staff | Create a new product | Product created |
| 3 | Staff | Enable stock management and set stock quantity | Stock = 3 |
| 4 | Staff | Publish the product | Product published |
| 5 | Customer (Guest) | Enter quantity 0 | Browser validation rejects the value |
| 6 | Customer (Guest) | Enter quantity 4 | Browser validation rejects the value |
| 7 | Customer (Guest) | Add quantity 2 to cart | Quantity 2 accepted |
| 8 | Customer (Guest) | Verify cart subtotal | THB 300 |
| 9 | Customer (Guest) | Change quantity from 2 to 1 | Subtotal THB 150 |
| 10 | Customer (Guest) | Remove the product | Cart becomes empty |
| 11 | Customer (Guest) | Return to the product and add quantity 2 again | Subtotal THB 300 |
| 12 | Customer (Guest) | Check My Account registration availability | Login only; registration unavailable |
| 13 | Customer (Guest) | Complete checkout using COD | Checkout successful |
| 14 | Customer (Guest) | Place the order | Order #446 created |
| 15 | Staff | Search for and verify the new order | Quantity 2; total THB 300 |
| 16 | Staff | Verify order status | Processing |
| 17 | Staff | Reopen product inventory | Remaining stock = 1 |

**Observed results:**

- Quantity 0 was rejected because the minimum quantity was 1.
- Quantity 4 was rejected because available stock was 3.
- Quantity 2 was accepted.
- Cart quantity update from 2 to 1 worked correctly.
- Product removal and empty cart verification passed.
- The product was successfully added again with quantity 2.
- The My Account page displayed login only, without a registration form. Conditional registration-related steps were recorded as Not Applicable (N/A).
- Order #446 was created successfully with quantity 2 and total THB 300.
- Order status was Processing.
- Remaining stock was 1 after checkout.

**Final execution result:** PASS  
**Recorded execution time:** 58.88 seconds

**Development issue:** During an early execution, the WordPress Admin Bar intercepted a click on the product category tab. Scrolling and element interaction were adjusted. The final recorded end-to-end execution passed.

## 4. Test Execution Summary

The following table summarizes the final recorded end-to-end test executions.

| Test ID | Scenario | Execution time | Result |
|---|---|---:|---|
| UI-001 | Product Discovery, Purchase and Order Management | 54.99 seconds | PASS |
| UI-002 | Coupon Validation and Discount | 51.89 seconds | PASS |
| UI-003 | Inventory Limits, Cart Changes and Guest Checkout | 58.88 seconds | PASS |

All three final recorded automated UI test executions completed successfully. These results refer to the recorded runs; they do not claim that the tests have been repeatedly executed across multiple runs.

Each end-to-end test creates new test data using a unique timestamp to avoid reusing previously created products, coupons, or orders.

## 5. How to Run the Tests

### 5.1 Prerequisites

- Python 3.12 or newer
- Google Chrome
- Selenium WebDriver / compatible ChromeDriver (Selenium Manager may manage the driver)
- Required Python packages

### 5.2 Activate the Virtual Environment

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5.3 Install Dependencies

```powershell
pip install pytest selenium python-dotenv
```

### 5.4 Configure Environment Variables

Create a local `.env` file:

```text
SHOP_ADMIN_USERNAME=your_username
SHOP_ADMIN_PASSWORD=your_password
```

Staff credentials must not be hardcoded in the scripts or committed to GitHub. Add `.env` to `.gitignore`.

### 5.5 Run Individual Test Scenarios

Run UI-001:

```powershell
pytest test_ui_001.py -v -s
```

Run UI-002:

```powershell
pytest test_ui_002.py -v -s
```

Run UI-003:

```powershell
pytest test_ui_003.py -v -s
```

### 5.6 Run All UI Tests

```powershell
pytest test_ui_001.py test_ui_002.py test_ui_003.py -v -s
```

**Note:** Each end-to-end execution creates new products and orders on the shared classroom server. UI-002 also creates a new coupon. Repeated executions may create additional records.

## 6. Test Evidence and Execution Records

Screen recordings and terminal screenshots should be saved for each full end-to-end test run. The recording should show the browser automation progressing through the staff, customer, and staff verification stages. Terminal screenshots should show the corresponding Pytest result.

### Evidence by Scenario

| Test | Screen recording should show | Terminal evidence |
|---|---|---|
| UI-001 | Product creation, guest product discovery, cart, checkout, order confirmation, and staff order verification | Final Pytest result showing `1 passed` |
| UI-002 | Product and coupon creation, invalid and valid coupon application, checkout, order confirmation, and staff order verification | Final Pytest result showing `1 passed` |
| UI-003 | Inventory setup, quantity validation, cart changes, checkout, order confirmation, staff order verification, and remaining stock | Final Pytest result showing `1 passed` and stock verification output |

### Evidence Folder Structure

```text
UI testing/
├── README.md
├── test_ui_001.py
├── test_ui_002.py
├── test_ui_003.py
└── evidence/
    ├── UI-001/
    │   ├── recording.mp4
    │   └── terminal_result.png
    ├── UI-002/
    │   ├── recording.mp4
    │   └── terminal_result.png
    └── UI-003/
        ├── recording.mp4
        └── terminal_result.png
```
https://drive.google.com/drive/folders/1y-bGTgWzoUtVq6qrdx0ZjnHi729Br4-9?usp=sharing