# ITCS386 Software Verification and Validation
# Project Phase 2

## 1. Project Overview

This project evaluates the WooCommerce online shop through four testing approaches: API Testing, System Testing, Automated UI Testing, and Performance Testing.

The objective is to verify the correctness of API operations, validate complete user workflows, automate user interactions through the web interface, and evaluate system performance under different load conditions.

**System Under Test:** WooCommerce Online Shop  
**Group:** liu-qi (G01)

## 2. Project Structure

```text
project phase 2/
│
├── README.md
│
├── API testing/
│
├── System testing/
│
├── UI testing/
│
└── Performance testing/
```

## 3. API Testing

### 3.1 Overview

API Testing verifies the functionality and correctness of WooCommerce API operations using automated tests.

**Tools and Technologies:**
- Python 3.12
- pytest
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

| Input Characteristic | Partition | Representative Value |
|---|---|---|
| Product Name | Valid | G01 Test Product CP01 |
| Product Type | Valid | `simple` |
| Product Type | Invalid | `invalid_type` |
| Regular Price | Valid | `199` |

**Test Case Selection**

| Test ID | Input Combination | Expected Result |
|---|---|---|
| CP01 | Valid Product Name + Valid Product Type + Valid Price | HTTP 201 Created |
| CP02 | Valid Product Name + Invalid Product Type + Valid Price | HTTP 400 Bad Request |

CP01 verifies that a product can be created using valid input values. CP02 changes the product type to an invalid value while keeping the other inputs valid to verify that the API rejects the invalid input.

#### 3.2.2 Update Product

**Endpoint:** `PUT /wp-json/wc/v3/products/{id}`

| Input Characteristic | Partition | Representative Value |
|---|---|---|
| Product ID | Existing Product | ID of a test product created by the test |
| Product Name | Valid | G01 Updated Product UP01 |
| Regular Price | Valid | `299` |

**Test Case Selection**

| Test ID | Input Combination | Expected Result |
|---|---|---|
| UP01 | Existing Product ID + Valid Product Name + Valid Price | HTTP 200 OK |

UP01 verifies that an existing test product can be updated successfully and that the response contains the updated product information.

#### 3.2.3 Add Item to Cart

**Endpoint:** `POST /wp-json/wc/store/v1/cart/add-item`

| Input Characteristic | Partition | Representative Value |
|---|---|---|
| Product ID | Purchasable Product | ID of an available product |
| Quantity | Valid | `1` |
| Cart Session | Initialized | Cart Token and Nonce obtained from the cart response |

**Test Case Selection**

| Test ID | Input Combination | Expected Result |
|---|---|---|
| AC01 | Purchasable Product + Valid Quantity + Initialized Cart Session | HTTP 201 Created |

AC01 verifies that a purchasable product can be added to an initialized shopping cart with a valid quantity.

### 3.3 Test Execution

All API tests are automated using pytest.

**Run all API tests:**

```bash
python -m pytest -v
```

**Run an individual test suite:**

```bash
python -m pytest tests/test_create_product.py -v
python -m pytest tests/test_update_product.py -v
python -m pytest tests/test_add_to_cart.py -v
```

### 3.4 Test Results

The recorded full test execution produced the following results:

| Metric | Result |
|---|---:|
| Total Test Cases | 4 |
| Passed | 4 |
| Failed | 0 |
| Execution Time | 1.34 seconds |

All four test cases passed in the recorded execution.

The full test output and execution evidence are stored in the `API testing/` directory.

### 3.5 Test Independence and Test Data

Each test should prepare the data and session it needs rather than relying on the execution order or data created by another test.

Test products created by the group use the `G01` prefix to distinguish them from demo products and other groups' data.

The Add Item to Cart test initializes its own cart session before adding a product. It does not place an order or complete checkout.

API credentials are stored in a local `.env` file and excluded from Git tracking.

### 3.6 Failure Analysis

Any failed test must be investigated to determine whether the cause is a system defect or an error in the test implementation.

For a confirmed system defect, document:
- The request sent to the API.
- The expected result.
- The actual result.

The test execution output and relevant evidence are stored in the `API testing/` directory.

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
