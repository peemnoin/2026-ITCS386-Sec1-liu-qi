# ITCS386 Software Verification and Validation

# Project Phase 2

## 1. Project Overview

This project evaluates the WooCommerce online shop through four testing approaches: API Testing, System Testing, Automated UI Testing, and Performance Testing.

The objective is to verify the correctness of API operations, validate complete user workflows, automate user interactions through the web interface, and evaluate system performance under different load conditions.

**System Under Test:** WooCommerce Online Shop

**Group:** liu-qi (G01)

## 2. Project Structure

```text
2026-ITCS386-Sec1-liu-qi/
│
├── liu-qi_project1/
│
├── project phase 2/
│   │
│   ├── README.md
│   │
│   ├── API testing/
│   │   ├── tests/
│   │   │   ├── test_add_to_cart.py
│   │   │   ├── test_create_product.py
│   │   │   └── test_update_product.py
│   │   │
│   │   ├── test_execution.png
│   │   ├── API_TEST_RESULTS.md
│   │   ├── check_api.py
│   │   ├── conftest.py
│   │   ├── pytest.ini
│   │   └── requirements.txt
│   │
│   ├── Performance testing/
│   │
│   ├── System testing/
│   │
│   └── UI testing/
│       ├── evidence/
│       │   ├── ui001/
│       │   │   └── terminal screenshot
│       │   ├── ui002/
│       │   │   └── terminal screenshot
│       │   └── ui003/
│       │       └── terminal screenshot
│       │
│       ├── README.md
│       ├── test_ui_001.py
│       ├── test_ui_002.py
│       ├── test_ui_003.py
│       └── requirements.txt
│
├── .gitignore
└── README.md
```

## 3. API Testing

### 3.1 Overview

API Testing verifies the functionality and correctness of WooCommerce API operations using automated tests.

**Tools and Technologies:**

- Python 3.12
- pytest 9.2.0
- Requests
- python-dotenv

Three API operations were selected. Each operation has its own automated test suite.

| Operation | API | HTTP Method |
|---|---|---|
| Create Product | WooCommerce REST API | POST |
| Update Product | WooCommerce REST API | PUT |
| Add Item to Cart | WooCommerce Store API | POST |

### 3.2 Test Design: Input Space Partitioning (ISP)

Input Space Partitioning (ISP) was used to design test inputs for each API operation.

The input characteristics were identified from the API request parameters. Their possible values were divided into partitions representing valid and invalid inputs. Representative values were then selected from these partitions to derive the test cases.

#### 3.2.1 Create Product

**Endpoint:** `POST /wp-json/wc/v3/products`

**Input Characteristics and Partitions**

| Input Characteristic | Partition | Representative Value |
|---|---|---|
| Product Name | Valid | G01 Test Product CP01 |
| Product Name | Empty | `""` |
| Product Name | Omitted | Field not included |
| Product Type | Valid | `simple` |
| Product Type | Invalid | `invalid_type` |
| Regular Price | Positive | `199` |
| Regular Price | Zero | `0` |
| Regular Price | Negative | `-100` |
| Regular Price | Empty | `""` |
| Regular Price | Non-numeric | `abc` |
| Regular Price | Omitted | Field not included |

**Test Case Coverage**

| Test ID | Input Condition | Expected Result |
|---|---|---|
| CP01 | Valid product data | HTTP 201 Created |
| CP02 | Invalid product type | HTTP 400 Bad Request |
| CP03 | Zero price | Product created with zero price |
| CP04 | Negative price | HTTP 400 Bad Request |
| CP05 | Empty price | Product created with empty price |
| CP06 | Non-numeric price | HTTP 400 Bad Request |
| CP07 | Omitted price | Product created with empty price |
| CP08 | Omitted name | Product created with default name `Product` |
| CP09 | Empty name | Product created with default name `Product` |

A total of 9 test cases were designed and executed for Create Product.

#### 3.2.2 Update Product

**Endpoint:** `PUT /wp-json/wc/v3/products/{id}`

**Input Characteristics and Partitions**

| Input Characteristic | Partition | Representative Value |
|---|---|---|
| Product ID | Existing Product | ID of a test product created by the test |
| Product ID | Non-existing | `99999999` |
| Product ID | Non-numeric | `abc` |
| Product ID | Zero | `0` |
| Product ID | Negative | `-1` |
| Product Name | Valid | G01 Updated Product UP01 |
| Product Name | Empty | `""` |
| Product Name | Omitted | Field not included |
| Regular Price | Positive | `299` |
| Regular Price | Zero | `0` |
| Regular Price | Negative | `-100` |
| Regular Price | Empty | `""` |
| Regular Price | Non-numeric | `abc` |
| Regular Price | Omitted | Field not included |
| Request Body | Empty | `{}` |

**Test Case Coverage**

| Test ID | Input Condition | Expected Result |
|---|---|---|
| UP01 | Existing ID + valid name and price | HTTP 200 OK |
| UP02 | Non-existing product ID | Invalid product ID error |
| UP03 | Non-numeric product ID | Route error |
| UP04 | Empty product name | Original name retained |
| UP05 | Negative price | HTTP 400 Bad Request |
| UP06 | Empty price | API response and product data validated |
| UP07 | Non-numeric price | HTTP 400 Bad Request; original price retained |
| UP08 | Empty request body | Original product data retained |
| UP09 | Zero product ID | Invalid product ID error |
| UP10 | Negative product ID | Route error |
| UP11 | Omitted product name | Original name retained |
| UP12 | Zero price | Product updated with zero price |
| UP13 | Omitted price | Original price retained |

A total of 13 test cases were designed and executed for Update Product.

#### 3.2.3 Add Item to Cart

**Endpoint:** `POST /wp-json/wc/store/v1/cart/add-item`

**Input Characteristics and Partitions**

| Input Characteristic | Partition | Representative Value |
|---|---|---|
| Product ID | Purchasable Product | ID of a test product created by the test |
| Product ID | Non-existing | `99999999` |
| Product ID | Non-numeric | `abc` |
| Product Purchase Status | Purchasable | Product with valid price |
| Product Purchase Status | Non-purchasable | Product with empty price |
| Quantity | Valid | `1` |
| Quantity | Zero | `0` |
| Quantity | Negative | `-1` |
| Quantity | Non-numeric | `abc` |
| Quantity | Omitted | Field not included |
| Cart Session | Initialized | Cart Token and Nonce obtained from the cart response |
| Request Header | Missing Nonce | Nonce header not included |

**Test Case Coverage**

| Test ID | Input Condition | Expected Result |
|---|---|---|
| AC01 | Purchasable product + quantity 1 + initialized cart | HTTP 201 Created |
| AC02 | Non-existing product ID | Invalid product error |
| AC03 | Non-numeric product ID | Invalid product error |
| AC04 | Non-purchasable product | Product not purchasable error |
| AC05 | Zero quantity | Invalid quantity error |
| AC06 | Negative quantity | Invalid quantity error |
| AC07 | Non-numeric quantity | Invalid parameter error |
| AC08 | Omitted quantity | Product added with default quantity 1 |
| AC09 | Missing Nonce header | Missing Nonce error |

A total of 9 test cases were designed and executed for Add Item to Cart.

### 3.3 Test Execution

All API tests are automated using pytest. The test suites can be executed together or individually.

**Run all API tests:**

```bash
python -m pytest tests -v
```

**Run an individual test suite:**

```bash
python -m pytest tests/test_create_product.py -v

python -m pytest tests/test_update_product.py -v

python -m pytest tests/test_add_to_cart.py -v
```

### 3.4 Test Results

All three API test suites were executed together.

**Execution Command:**

```bash
python -m pytest tests -v
```

**Overall Test Results**

| Test Suite | Total Test Cases | Passed | Failed |
|---|---:|---:|---:|
| Create Product | 9 | 7 | 2 |
| Update Product | 13 | 11 | 2 |
| Add Item to Cart | 9 | 9 | 0 |
| **Total** | **31** | **27** | **4** |

**Execution Time:** 11.40 seconds

**Overall Result:** 27 passed, 4 failed.

The four failed test cases revealed API behaviors that did not meet the price validation requirements defined by the project team. They are documented as system defects rather than test implementation errors.

The detailed test results are documented in [`API_TEST_RESULTS.md`](API%20testing/API_TEST_RESULTS.md).

The test execution screenshot is available at [`test_execution.png`](API%20testing/test_execution.png).

### 3.5 Test Independence and Test Data

Each test prepares the data and session it needs rather than relying on the execution order or data created by another test.

Shared fixtures in `conftest.py` manage API authentication, product creation, and test data cleanup.

Test products created by the group use the `G01` prefix to distinguish them from demo products and other groups' data.

The product cleanup fixture records the IDs of products created during each test and attempts to delete them after the test finishes, including when a test fails.

The Add Item to Cart tests initialize their own cart sessions before sending requests. Test products created for the relevant cart test cases are cleaned up after execution.

The Add Item to Cart tests do not place an order or complete checkout.

API credentials are stored in a local `.env` file and excluded from Git tracking.

### 3.6 Failure Analysis

The latest API test execution identified four defects related to product price validation:

| Defect ID | Related Test Case | Expected Result | Actual Result |
|---|---|---|---|
| DEF-API-01 | CP04 | Creating a product with a negative price returns HTTP 400 | HTTP 201; API accepted `-100` |
| DEF-API-02 | CP06 | Creating a product with a non-numeric price returns HTTP 400 | HTTP 201; API stored an empty price |
| DEF-API-03 | UP05 | Updating a product with a negative price returns HTTP 400 | HTTP 200; API accepted `-100` |
| DEF-API-04 | UP07 | Updating a product with a non-numeric price returns HTTP 400 and retains the original price | HTTP 200; API cleared the original price |

These defects are evaluated against the project team's requirement that product prices must be numeric and non-negative. The test failures therefore represent mismatches between the observed API behavior and the team's expected validation rules.

The test execution output and detailed defect evidence are documented in `API testing/API_TEST_RESULTS.md` and the `API testing/` directory.

## 4. System Testing

**Objective:** Verify end-to-end Staff → Customer → Staff workflows using manual testing and Cash on Delivery (COD).

**Tools and Techniques:** Separate staff admin and guest customer browser sessions, step-by-step test cases, screenshots, and requirement traceability.

### 4.1 Execution and Evidence

The three manual scenarios were executed on **11 November 2026**. A **read-only inspection on 18 November 2026** added screenshots E01–E13 of the existing orders, coupon and stock records. This supplement verifies the recorded outcomes below; it is not a new manual checkout run. A separate **targeted manual re-execution of SYS-001 Step 10 on 18 November, 19:58–20:00**, verified guest Checkout → native browser Back without submitting an order. Automated UI executions are reported separately in Section 5.

**The main purchase, discount and stock workflows are supported by evidence.** Missing evidence for individual additional checks does not mean those workflows failed. The original coupon naming deviation is a test-data issue, not a confirmed WooCommerce defect.

### 4.2 Test Cases and Verified Outcomes

| Case ID | Workflow | Verified result, including 18 Nov evidence | Remaining evidence limits |
|---|---|---|---|
| **SYS-001** | Create Mug at THB 199 → buy 2 via COD → verify and complete order. | **Purchase and staff order verification passed (14 PASS / 2 N/A / 0 NOT VERIFIED).** Order `#127` totals THB 398 and is `Completed`. E01–E03 and E13 resolve the obscured final-order evidence for Step 16. **Step 10 PASS on targeted 18 Nov rerun:** native Back retained Mug x2 / THB 398, without reload; no new submitted order observed (S01–S05). | Step 4 search is **N/A** (guest storefront has no visible search bar). Guest My Account history is **N/A**. Original Nov 11 Step 10 evidence remains historical; the new run closes the current gap. |
| **SYS-002** | Create Tee at THB 200 and 10% coupon → reject invalid code → apply/remove/reapply coupon → buy 2 via COD → inspect order/coupon. | **Coupon calculation and order verification passed (12 PASS / 1 NOT VERIFIED).** THB 400 − 40 = 360 for Order `#139`. Step 2 is **PASS** functionally; Coupon `#138` currently has the G01 prefix (`G01-GV82WTW5`), percentage type and amount 10 (E05–E06); current usage is 2 (E07). | Original code `gv82wtw5` is retained only as a historical naming note, not an application failure. Step 8 navigation persistence remains NOT VERIFIED. |
| **SYS-003** | Create product at THB 150, stock 3 → reject quantities 0/4 → update/remove/re-add cart → buy 2 → inspect stock. | **Quantity checks, purchase and stock reduction passed (13 PASS / 4 N/A / 0 NOT VERIFIED).** Step 2 product detail is **PASS** via catalog (`Sys003-2.png`; no visible storefront search bar). Order `#142` totals THB 300. Step 16 is **verified retrospectively on 18 Nov**: order notes record stock 3→1 (E08); admin/storefront show 1 (E10–E12). | Storefront search bar and conditional registration/account steps are **N/A** because no search bar or registration form was available in the observed flow. |

**SYS-001 Step 10 — PASS (targeted execution, 18 Nov 2026):** In a fresh Chrome Incognito guest session, the cart held `G01_SYS001_20261111_01 Mug` x2 for THB 398. Proceed to Checkout showed the same quantity/total with empty contact/billing fields. Clicking the native browser Back button returned to `/cart/` with the same items and THB 398, without a reload or recovery. No order was submitted; the refreshed admin list remained at 129 orders, newest visible #975. This supports no new submitted order observed, rather than a database-level assertion about hidden drafts. [S01–S05 and execution notes](System%20testing/screenshots/sys001-step10-2026-11-18/EVIDENCE_INDEX.md). The old empty-cart screenshot is retained as history; this is a new Step 10 execution, not a full scenario rerun.

**SYS-002 naming clarification:** The November 18 screenshots verify that the current coupon has the G01 prefix. Order `#139` retains the original code. The earlier Step 2 FAIL label referred to the planned naming convention; it must not be summarized as a failed discount feature. The workbook now separates the successful coupon function from that historical data deviation. Usage `2 / ∞` is a verified current value, but it does not establish the exact before/after increment caused by this order.

### 4.3 Requirement Traceability and Evidence

- [Test cases and RTM workbook](System%20testing/test_cases/G01_System_Testing_Results_and_RTM.xlsx): step-level expectations, results, historical notes and the dated retrospective supplement.
- [System Testing details](System%20testing/README.md) and [E01–E13 evidence index](System%20testing/screenshots/retrospective-2026-11-18/EVIDENCE_INDEX.md).
- Original screenshots remain in `System testing/screenshots/SYS-001/`, `SYS-002/` and `SYS-003/`; selected privacy-redacted copies are in `screenshots/redacted/`.

The RTM distinguishes tested functions from full feature coverage. Purchase/COD, core cart actions, discount calculation, order management and the observed stock reduction are evidenced. SYS-001 pre-submit Back is now verified. Storefront search bar and public account registration are **N/A** (not exposed in the observed guest UI). SYS-002 navigation persistence and order-specific coupon usage attribution still have evidence gaps. Paging, variations and staff edit/delete are not fully covered. These limits do not invalidate the successful checks above.

## 5. Automated UI Testing

### 5.1 Overview

Automated UI Testing verifies the three selected System Testing scenarios through the WooCommerce web interface using Selenium WebDriver.

Each automated test follows an end-to-end **Staff → Customer → Staff** workflow and verifies the results displayed on the pages rather than only performing UI actions.

**Tools and Technologies:**

- Python 3.12
- Pytest
- Selenium WebDriver
- Google Chrome
- python-dotenv

Separate browser sessions are used for staff and guest customer activities. Each execution creates unique timestamp-based test data to avoid conflicts with products, coupons, and orders from previous runs.

### 5.2 Automated Test Cases

| UI Test | Automated From | What the Automation Verifies |
|---|---|---|
| UI-001 | SYS-001 | Product/category, quantity, cart and checkout total, Checkout → Back retention without unintended order creation, COD checkout, order details, and final order status (`Processing` → `Completed`) |
| UI-002 | SYS-002 | Invalid and valid `G01` coupon behavior, discount calculation, coupon removal/reapplication, navigation persistence, checkout total, staff order verification, and coupon usage count |
| UI-003 | SYS-003 | Quantity boundaries (`0`, `4`), cart update/remove/re-add, checkout, order status, and hard assertion that remaining stock equals `1` |

The tests use explicit waits and stable element locators such as IDs, names, and CSS selectors for dynamic page interactions, plus `--disable-features=HttpsUpgrades,HttpsFirstBalancedModeAutoEnable` for the plain-HTTP test server.

### 5.3 Test Results

Earlier single-run executions (`2026-11-14`) passed all three tests (`UI-001` Order `#449` in `73.43s`, `UI-002` Order `#452` in `61.41s`, `UI-003` Order `#454` in `62.21s`). After strengthening assertions on `2026-11-18`, Run 1 attempt 1 (`2026-11-18 17:06–17:08`) passed `UI-001` (`Order #889`, Completed) and `UI-003` (`Order #893`, stock `1`), while `UI-002` failed at coupon `#publish` (subsequently fixed locally in `test_ui_002.py`). **Two consecutive passing runs of the final updated UI code remain `NOT VERIFIED`.**

| UI Test | Latest Evidenced Result | Status |
|---|---|---|
| UI-001 | `2026-11-18`: Two items purchased for THB 398 (`Order #889`), Checkout → Back (`native_back`) and no unintended order verified, status updated `Processing` → `Completed`. | PASS |
| UI-002 | `2026-11-14`: Invalid coupon rejected, 10% coupon reduced THB 400 to THB 360 (`Order #452`). `2026-11-18` Run 1 failed at coupon `#publish` before local fix; updated coupon-removal/reapply/usage assertions not yet re-run. | NOT VERIFIED (updated code) |
| UI-003 | `2026-11-18`: Quantities `0` and `4` rejected, cart update/remove/re-add verified, `Order #893` (THB 300, `Processing`) created, and hard assertion `post_order_stock == "1"` passed. | PASS |

The automated tests verify visible page results such as cart and checkout totals, coupon discounts, order details and status, browser quantity validation, and inventory changes.

### 5.4 Observed Limitations

During UI-001, the guest storefront did not display a visible Search Bar. This limitation was recorded, and the newly created product was located through shop pagination instead.

During UI-003, the public My Account page displayed a Login form only and did not provide a customer registration form. Conditional registration-related steps were therefore treated as **N/A**, and no system configuration was changed.

Two consecutive passing runs of the final updated UI suite (`test_ui_001.py`, `test_ui_002.py`, `test_ui_003.py`) have not yet been completed and recorded.

### 5.5 How to Run

From the `UI testing/` directory, run all three automated UI tests with:

```bash
pytest test_ui_001.py test_ui_002.py test_ui_003.py -v -s
```

Individual scenarios can also be executed with:

```bash
pytest test_ui_001.py -v -s
pytest test_ui_002.py -v -s
pytest test_ui_003.py -v -s
```

Staff credentials are loaded from a local `.env` file and are not stored directly in the test scripts.

### 5.6 Test Evidence

Terminal screenshots (`2026-11-14` runs in [`UI testing/evidence/`](UI%20testing/evidence/))

https://drive.google.com/drive/folders/1y-bGTgWzoUtVq6qrdx0ZjnHi729Br4-9?usp=sharing

The evidence demonstrates the automated **Staff → Customer → Staff** workflows, page-level verification, and Pytest results.

Detailed test data, end-to-end flows, parity mapping, scripts, execution instructions, and evidence are documented in [`UI testing/README.md`](UI%20testing/README.md).


## 6. Performance Testing

### 6.1 Overview

The scripts and the k6 summary of every run are in the `Performance testing/` folder. Result files are in `Performance testing/results/`.

**User scenario:** every script follows the same steps as a real visitor:

1. Open the shop home page.
2. Search for a product (`?s=shirt&post_type=product`).
3. Open one of two product pages (Album or Beanie with Logo), chosen at random.

Each virtual user waits 1 to 3 seconds between steps (0.5 to 1.5 seconds in the stress and spike tests). The scripts do not add items to the cart or place orders, because orders stay on the shared server for all groups.

| Test | Script | Virtual users (VUs) | Duration | Run date and time | Result files |
|---|---|---|---|---|---|
| Average-load | `avg_load_test.js` | 0 to 20 in 1 min, 20 for 5 min, then down | 7 min | 16 Nov 2026, 20:58 | `avg_load_20261116_2058.*` |
| Stress | `stress_test.js` | 20, 40, 60, 80, 100 (2 min per step), then down | 11 min | 16 Nov 2026, 21:09 | `stress_20261116_2109.*` (includes `.csv`) |
| Constant-load checks | `avg_load_test.js` with `--stage` | 5, 10, 12, 13, 15 (30 s ramp-up, then 2 min) | 2.5 min each | 16 Nov 2026, 21:34 to 21:47 | `vu05_*`, `vu10_*`, `vu12_*`, `vu13_*`, `vu15_*` |
| Spike | `spike_test.js` | 5 for 1 min, jump to 50 in 10 s, hold 1 min, back to 5 for 5 min | about 7.5 min | 16 Nov 2026, 23:11 | `spike_20261116_2311.*` (includes `.csv`) |
| Soak | `soak_test.js` | 10 for 56 min (2 min ramp up and down) | 60 min | 16 Nov 2026, 23:33 | `soak_20261116_2333.*` (includes `.csv`) |
| Average-load (repeat) | `avg_load_test.js` | same as above | 7 min | 18 Nov 2026, 17:35 | `avg_load_20261118_1735.*` |
| Stress (repeat) | `stress_test.js` | same as above | 11 min | 18 Nov 2026, 17:42 | `stress_20261118_1735.*` |
| Spike (repeat) | `spike_test.js` | same as above | about 7.5 min | 18 Nov 2026, 17:53 | `spike_20261118_1735.*` |
| Soak (repeat) | `soak_test.js` | same as above | 60 min | 18 Nov 2026, 18:01 | `soak_20261118_1735.*` |

We added the constant-load checks because the stress test only showed that the response time went above 1 second somewhere between 8 and 12 VUs. Running a fixed number of VUs for 2 minutes gave a clearer answer.

**Result files.** Each run has a `.txt` file (the full k6 terminal output) and a `.json` file (the k6 summary). The stress, spike and soak runs also have a `.csv` file with the result of every request, which we used to measure the results over time. `report.html` is a one-page report of all runs. Open it in a web browser to see the tables and the response time charts. It has one tab for the 16 November runs and one tab for the 18 November runs.

### 6.2 Thresholds, virtual users and duration

Every script has two thresholds:

- `http_req_duration: p(95) < 1000 ms`. The project asks when the response time goes above 1 second, so we used 1 second as the limit. We used p(95) instead of the average, because the average can hide a small number of very slow requests.
- `http_req_failed: rate < 1%` for the average-load and soak tests, because under normal load almost no request should fail. We used `rate < 5%` for the stress and spike tests, because these tests push the system past normal load on purpose, so some errors are expected.

**Virtual users and duration:**

- Average-load: we had no real traffic data, so we chose 20 VUs as a busy but normal number for a small shop. 5 minutes at a steady load is long enough to get stable results.
- Stress: steps of 20 VUs up to 100, 2 minutes each, so we can see at which step the system starts to have problems.
- Spike: the average-load and stress tests showed that the shop can serve about 12 VUs, so a jump from 5 to 50 VUs in 10 seconds (about 4 times this limit) copies a sudden rush of users. The 5 minutes after the spike let us measure the recovery time.
- Soak: we used 10 VUs, because at 10 VUs p(95) was still under 1 second (0.84 s). If the shop becomes slower over time, we can see it cross the limit. One hour is long enough to see this.

### 6.3 Results

| Run | vus_max | p(95) | Median | Max | http_req_failed | Requests/s | Duration threshold |
|---|---:|---:|---:|---:|---:|---:|---|
| Constant 5 VUs | 5 | 0.56 s | 0.34 s | 1.18 s | 0.00% | 1.84 | Passed |
| Constant 10 VUs | 10 | 0.84 s | 0.38 s | 1.30 s | 0.00% | 3.64 | Passed |
| Constant 12 VUs | 12 | 0.96 s | 0.45 s | 1.69 s | 0.00% | 4.23 | Passed |
| Constant 13 VUs | 13 | 1.01 s | 0.48 s | 3.17 s | 0.00% | 4.55 | Failed |
| Constant 15 VUs | 15 | 1.40 s | 0.54 s | 2.32 s | 0.00% | 4.94 | Failed |
| Average-load (20 VUs) | 20 | 3.38 s | 1.63 s | 5.02 s | 0.00% | 4.65 | Failed |
| Stress (up to 100 VUs) | 100 | 21.60 s | 8.64 s | 60.00 s | 0.25% | 4.73 | Failed |
| Spike (5 to 50 VUs) | 50 | 10.0 s | 0.36 s | 14.37 s | 0.00% | 3.79 | Failed |
| Soak (10 VUs, 1 hour) | 10 | 0.66 s | 0.33 s | 1.44 s | 0.00% | 4.08 | Passed |


**Stress test by step.** We used the `.csv` output to measure the last 60 seconds of each step:

| Step | p(95) | Median | Requests/s |
|---|---:|---:|---:|
| 20 VUs | 3.40 s | 1.63 s | 5.37 |
| 40 VUs | 8.39 s | 5.33 s | 5.23 |
| 60 VUs | 16.08 s | 9.68 s | 4.73 |
| 80 VUs | 17.71 s | 13.27 s | 5.13 |
| 100 VUs | 25.50 s | 17.36 s | 4.52 |

**Changes between runs.** We repeated all four tests on 18 November 2026 (17:35 to 19:01). The file names use the start time of the first test, 17:35. The results were close to the 16 November runs: p(95) was 2.85 s in the average-load test (3.38 s before), 22.06 s in the stress test (21.60 s), 10.38 s in the spike test (10.00 s) and 0.69 s in the soak test (0.66 s). The only clear change was in the stress test: no request failed on 18 November, while 8 requests timed out on 16 November. This may be because fewer groups were testing at the same time. Our answers above use the 16 November runs. `report.html` shows the charts for both days.

At 20 VUs, the average-load test (p(95) 3.38 s) and the 20 VU step of the stress test (p(95) 3.40 s) gave almost the same result, so our runs on 16 November were consistent. All groups share one server, and we ran our tests in the evening, a few days before the progress presentation. Other groups may have been testing at the same time, so the results may be different on another day.

### 6.4 Answers to the questions

**How many virtual users can the system serve before the response time goes above 1 second?**

About 12 VUs. At 12 VUs, p(95) was 961 ms. At 13 VUs, it was 1,005 ms, which is just above the limit. Both values are very close to 1 second, so on a busier or quieter day the limit may move by one or two users.

**In the stress test, at how many virtual users does the system start to show problems?**

The system starts to show problems at about 13 VUs, where p(95) goes above 1 second (1,005 ms). The response time keeps getting worse as we add more users: p(95) was 3.40 s at 20 VUs and 25.50 s at 100 VUs. Errors start only at 95 to 100 VUs, where 8 requests (0.25%) failed with a timeout.

**In the soak test, do the response time or the error rate get worse as the test goes on?**

No. In the first full 5 minutes at 10 VUs (300-600 s), p(95) was 0.65 s, and in the last full 5 minutes at 10 VUs (3000-3300 s) it was 0.62 s. `http_req_failed` stayed at 0.00% for the whole hour. The response time went up and down a little (between 0.59 s and 0.73 s), but it did not keep growing, so we did not see the shop become slower over time.

**In the spike test, how long does the system take to return to normal service after the spike?**

Before the spike, during the first minute (up to 5 VUs), p(95) was about 0.4 s. During the spike, at 50 VUs, it rose to about 12 s, and no request failed. The spike ended 140 seconds after the start. p(95) went back under 1 second and stayed there from about 180 seconds, so the shop took about 40 seconds to return to normal service. We measured this from the `.csv` output in 30-second windows, so the value is accurate to about 30 seconds.

**What do http_req_failed, http_req_duration and vus_max tell you about the system in each test?**

- Average-load: `http_req_failed` was 0.00%, so the shop answered every request. `http_req_duration` p(95) was 3.38 s, so the shop is too slow for 20 users at the same time. `vus_max` was 20, so the test reached the planned load.
- Stress: `http_req_failed` was 0.25%, and all failures were timeouts at the highest load. `http_req_duration` p(95) was 21.6 s and the maximum was 60 s, so users would wait a very long time. `vus_max` was 100, so the test reached the highest step.
- Spike: `http_req_failed` was 0.00%, so the shop answered every request, but slowly. `http_req_duration` p(95) was 10.0 s, which shows how much slower the shop became during the sudden rush. `vus_max` was 50, so the test reached the planned spike.
- Soak: `http_req_failed` was 0.00%, so the shop stayed available for the whole hour. `http_req_duration` p(95) was 0.66 s, under our 1-second limit. `vus_max` was 10, so the test kept the planned load for one hour.

### 6.5 How to run

Install k6 (for example `brew install k6` on macOS), then run the commands from the `Performance testing/` folder:

```bash
mkdir -p results
k6 run avg_load_test.js --summary-export "results/avg_load_$(date +%Y%m%d_%H%M).json" | tee "results/avg_load_$(date +%Y%m%d_%H%M).txt"
k6 run stress_test.js --out csv="results/stress_$(date +%Y%m%d_%H%M).csv" --summary-export "results/stress_$(date +%Y%m%d_%H%M).json" | tee "results/stress_$(date +%Y%m%d_%H%M).txt"
k6 run spike_test.js --out csv="results/spike_$(date +%Y%m%d_%H%M).csv" --summary-export "results/spike_$(date +%Y%m%d_%H%M).json" | tee "results/spike_$(date +%Y%m%d_%H%M).txt"
k6 run soak_test.js --out csv="results/soak_$(date +%Y%m%d_%H%M).csv" --summary-export "results/soak_$(date +%Y%m%d_%H%M).json" | tee "results/soak_$(date +%Y%m%d_%H%M).txt"
```

Constant-load check (example with 12 VUs):

```bash
k6 run --stage 30s:12 --stage 2m:12 avg_load_test.js --summary-export "results/vu12_$(date +%Y%m%d_%H%M).json" | tee "results/vu12_$(date +%Y%m%d_%H%M).txt"
```

k6 shows `thresholds on metrics 'http_req_duration' have been crossed` when the response time is above our limit. This is a test result, not an error in the script.


## 7. Team Information

**Course:** ITCS386 Software Verification and Validation

**Group:** liu-qi (G01)

### Responsibilities

| Member | Student ID | Responsibilities |
|---|---|---|
| Sunattha Boonl-or | 6688009 | Performance testing (k6): average-load and stress tests, and analysed at which point the response time goes above 1 second. |
| Tinakome Rasripenngam | 6688095 | Performance testing (k6): spike and soak tests, analysed the recovery time and performance degradation, and combined the performance testing results. |
| Veerakron No-in | 6688164 | Automated UI testing: helped Wirunya plan the test case structure from the start, chose 3 system test cases to automate with Selenium WebDriver, and saved screenshots and recordings. |
| Wirunya Kaewthong | 6688172 | System testing: designed at least 3 manual test case scenarios, created the requirement traceability matrix, tested both the staff and customer sides, and recorded the results with screenshots. |
| Piyada Chalermnontakarn | 6688239 | API testing: tested 3 API operations with pytest, designed test inputs with input space partitioning, and wrote the test results and defect analysis. |

## 8. Repository

GitHub Repository:

https://github.com/peemnoin/2026-ITCS386-Sec1-liu-qi
