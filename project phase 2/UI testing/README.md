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
**Recorded execution time:** 73.43 seconds (terminal screenshot `evidence/ui001/Screenshot 2026-11-14 003703.png`, Order `#449`; an earlier run recorded 54.99 seconds)

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
**Recorded execution time:** 61.41 seconds (terminal screenshot `evidence/ui002/Screenshot 2026-11-14 003944.png`, Order `#452`; an earlier run recorded 51.89 seconds)

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
| 14 | Customer (Guest) | Place the order | Order created (Order `#454` in `2026-11-14` screenshot; `#446` in earlier run) |
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
- Order `#454` (`2026-11-14` terminal screenshot; `#446` in earlier run) was created successfully with quantity 2 and total THB 300.
- Order status was Processing.
- Remaining stock was 1 after checkout.

**Final execution result:** PASS  
**Recorded execution time:** 62.21 seconds (terminal screenshot `evidence/ui003/Screenshot 2026-11-14 004015.png`; an earlier run recorded 58.88 seconds)

**Development issue:** During an early execution, the WordPress Admin Bar intercepted a click on the product category tab. Scrolling and element interaction were adjusted. The final recorded end-to-end execution passed.

## 4. Test Execution Summary

**Final repeatability evidence (25 November 2026).** Each automated UI test was run twice in a row with the same final code, and every run passed. Each run created a new product, coupon and order with a timestamp in the name, so the second run did not reuse data from the first run. The full pytest output of every run is saved in [`evidence/repeatability/`](evidence/repeatability/).

| UI Test | Run 1 | Run 2 | Status |
|---|---|---|---|
| UI-001 | 15:07, Order `#1881`: 2 items, THB 398, status `Completed` (75.20 s) | 15:09, Order `#1883`: same result (71.93 s) | PASS on both runs |
| UI-002 | 15:03, Order `#1876`: THB 400 to THB 360 with the 10% coupon, coupon usage 0 to 1 (37.76 s) | 15:04, Order `#1879`: same result (37.93 s) | PASS on both runs |
| UI-003 | 14:53, Order `#1869`: quantities 0 and 4 rejected, stock 3 to 1 (77.69 s) | 15:00, Order `#1871`: same result (35.84 s) | PASS on both runs |

**Test code fixes before the final runs.** On 25 November we fixed problems in the test code, not in the shop:

- Select-all key: the tests use Cmd+A on macOS and Ctrl+A on Windows (`SELECT_ALL_KEY`), because they were first written on Windows.
- Publish: if WordPress ignores the first click on Publish, the test clicks again (up to 3 times) and waits for the saved post page (`_publish_and_wait`).
- UI-001: opens the Accessories category with "Sort by latest", because the category now has many products and the new product was not on page 1. It also waits for the order search results before opening the order.
- UI-002: after removing the coupon, it checks the coupon chip and the discount row (the "removed" message still shows the code), and it opens the "Add coupons" panel again before reapplying the coupon.
- UI-003: retries the staff login once when the shared server is slow.
- Longer waits (up to 120 s) because the shared server was slow on the deadline day.

### Earlier single runs (history)

The table below shows earlier single runs from 14 November 2026, before the fixes above.

| Test ID | Scenario | Execution time (2026-11-14 evidence) | Result |
|---|---|---:|---|
| UI-001 | Product Discovery, Purchase and Order Management | 73.43 seconds (Order `#449`) | PASS |
| UI-002 | Coupon Validation and Discount | 61.41 seconds (Order `#452`) | PASS |
| UI-003 | Inventory Limits, Cart Changes and Guest Checkout | 62.21 seconds (Order `#454`) | PASS |

All three earlier end-to-end executions (2026-11-14) completed successfully. The final two-run repeatability evidence from 25 November is shown at the start of this section.

### 4.1 Manual-to-Automated Parity Mapping

| Manual Case & Steps | Automated Script | Disposition | Parity & Assertion Notes |
|---|---|---|---|
| `SYS-001` Steps 1–3, 5–9, 11–14, 16 | `test_ui_001.py` | **Implemented** | Staff create (`199`, stock `10`, `Accessories`), category/sort, qty `2` (`฿398.00`), COD order, `Processing -> Completed`, final list check. |
| `SYS-001` Step 4 (Search) | `test_ui_001.py` | **Conditional / Fallback** | Checks for visible Search Bar, logs `Step 4 FAIL: Guest storefront has no visible Search Bar`, falls back to pagination. |
| `SYS-001` Step 10 (Checkout → Back) | `test_ui_001.py` | **Implemented** | Navigates Checkout → Back, distinguishes `native_back` vs `reload_recovery`, asserts URL `/cart/` (not `order-received`), qty `2`, `฿398.00`. |
| `SYS-001` Step 15 (Guest My Account) | `test_ui_001.py` | **N/A** | Guest My Account requires login; order verified via confirmation + Staff Admin. |
| `SYS-002` Steps 1–5, 9–11, 13 | `test_ui_002.py` | **Implemented** | Staff creates `G01` product (`200`) & `G01` 10% coupon, tests invalid + valid coupon (`400 -> 360`), COD checkout, Staff order check. *(Uses `Accessories` vs manual `Clothing/Tshirts`.)* |
| `SYS-002` Steps 6–8 (Remove, Reapply, Navigate) | `test_ui_002.py` | **Implemented (2026-11-18)** | Added coupon removal (`400.00`, discount absent), reapplication (`40.00`, `360.00`), and product-page navigate away/back persistence. |
| `SYS-002` Step 12 (Coupon Usage Count) | `test_ui_002.py` | **Implemented (2026-11-18)** | Records baseline usage (`0`) and asserts `post_coupon_usage == initial_coupon_usage + 1` in `wp-admin`. |
| `SYS-003` Steps 1, 3–8, 12–13, 15 | `test_ui_003.py` | **Implemented** | Managed stock `3`, qty `0` & `4` `checkValidity()`, cart update/remove/re-add, COD checkout, Staff order check (`Processing`, qty `2`, `300.00`). |
| `SYS-003` Step 2 (Search) | `test_ui_003.py` | **Pagination Fallback** | Locates product via shop pagination. |
| `SYS-003` Steps 9–11, 14, 17 (Registration) | `test_ui_003.py` | **Conditional / N/A** | Verifies My Account is login-only; treats registration steps as `N/A`. |
| `SYS-003` Step 16 (Post-checkout Stock) | `test_ui_003.py` | **Implemented (2026-11-18)** | Hard `assert post_order_stock == "1"` after bounded refresh. |

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
├── requirements.txt
├── test_browser.py          # initial browser smoke-test script (not part of UI-001..003)
├── test_ui_001.py
├── test_ui_002.py
├── test_ui_003.py
└── evidence/
    ├── ui001/
    │   ├── Screenshot 2026-11-14 003613.png
    │   ├── Screenshot 2026-11-14 003632.png
    │   ├── Screenshot 2026-11-14 003649.png
    │   └── Screenshot 2026-11-14 003703.png
    ├── ui002/
    │   ├── Screenshot 2026-11-14 003859.png
    │   ├── Screenshot 2026-11-14 003916.png
    │   ├── Screenshot 2026-11-14 003926.png
    │   └── Screenshot 2026-11-14 003944.png
    ├── ui003/
    │   ├── Screenshot 2026-11-14 003959.png
    │   └── Screenshot 2026-11-14 004015.png
    └── repeatability/       # final evidence, 25 Nov 2026: two passing runs per test
        ├── ui001_run1.txt, ui001_run2.txt
        ├── ui002_run1.txt, ui002_run2.txt
        └── ui003_run1.txt, ui003_run2.txt
```
Screen recordings (`.mp4`) are hosted externally on Google Drive due to file size:
https://drive.google.com/drive/folders/1y-bGTgWzoUtVq6qrdx0ZjnHi729Br4-9?usp=sharing