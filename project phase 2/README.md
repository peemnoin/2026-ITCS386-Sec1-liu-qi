
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
│   │   ├── api_test_execution.png
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

The test execution screenshot is available at [`api_test_execution.png`](API%20testing/api_test_execution.png).

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

**Objective:** Verify complete end-to-end workflows across the staff and customer sides of the WooCommerce shop.

**Tools and Techniques:** Manual testing

**Test Cases:** [To be completed]

**Requirement Traceability Matrix:** [To be completed]

**Test Results and Evidence:** [To be completed]

For detailed test cases, screenshots, and results, see the `System testing/` directory.

## 5. Automated UI Testing

**Objective:** Automate selected system test scenarios through the WooCommerce user interface and verify the results displayed on the pages.

**Tools and Technologies:** [To be completed]

**Automated Test Cases:** [To be completed]

**Test Results and Evidence:** [To be completed]

For scripts and execution evidence, see the `UI testing/` directory.

## 6. Performance Testing

**Objective:** Evaluate the performance of the WooCommerce shop under different workload conditions.

**Tools and Technologies:** k6

**Test Types:**

- Average-load test
- Stress test
- Soak test
- Spike test

**Test Results and Analysis:** [To be completed]

For scripts, K6 summaries, and performance analysis, see the `Performance testing/` directory.

## 7. Team Information

**Course:** ITCS386 Software Verification and Validation

**Group:** liu-qi (G01)

**Group Members:** [To be completed]

## 8. Repository

GitHub Repository:

https://github.com/peemnoin/2026-ITCS386-Sec1-liu-qi
