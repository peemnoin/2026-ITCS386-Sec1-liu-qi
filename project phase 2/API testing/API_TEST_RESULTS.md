# API Testing Results

## 1. Overview

This document summarizes the results of API testing for Project 2. The tests were implemented using **Python, pytest, and requests** to verify the functionality and error handling of the WooCommerce REST API and Store API.

The API testing covers three main operations:

1. **Create Product** – Testing product creation with valid and invalid input values.
2. **Update Product** – Testing product updates using different product IDs and input conditions.
3. **Add to Cart** – Testing adding products to the shopping cart with valid and invalid product IDs, quantities, and request headers.

## 2. Test Environment

| Item | Configuration |
|---|---|
| Operating System | Windows |
| Programming Language | Python 3.12.2 |
| Testing Framework | pytest 9.2.0 |
| HTTP Library | requests |
| API | WooCommerce REST API / Store API |
| Test Execution | `python -m pytest tests -v` |

## 3. Test Suites

### 3.1 Create Product

**Test File:** `tests/test_create_product.py`

**Objective:** Verify that the API can create products and handle different input conditions.

| Test Case | Description | Expected Result |
|---|---|---|
| CP01 | Create product with valid data | Product is created successfully |
| CP02 | Create product with invalid product type | API returns an error response |
| CP03 | Create product with zero price | Product is created with zero price |
| CP04 | Create product with negative price | API response is validated |
| CP05 | Create product with empty price | API response is validated |
| CP06 | Create product with non-numeric price | API response is validated |
| CP07 | Create product without price | API response is validated |
| CP08 | Create product without name | API response is validated |
| CP09 | Create product with empty name | API response is validated |

**Result:** 9 passed.

### 3.2 Update Product

**Test File:** `tests/test_update_product.py`

**Objective:** Verify that the API can update existing products and handle invalid product IDs and different input conditions.

| Test Case | Description | Expected Result |
|---|---|---|
| UP01 | Update product with valid data | Product is updated successfully |
| UP02 | Update product with non-existing ID | API returns an invalid product ID error |
| UP03 | Update product with non-numeric ID | API returns a route error |
| UP04 | Update product with empty name | Original name is retained |
| UP05 | Update product with negative price | API response is validated |
| UP06 | Update product with empty price | API response is validated |
| UP07 | Update product with non-numeric price | API response is validated |
| UP08 | Update product with empty request body | Original product data is retained |
| UP09 | Update product with zero ID | API returns an invalid product ID error |
| UP10 | Update product with negative ID | API returns a route error |
| UP11 | Update product with alphanumeric ID | API returns a route error |
| UP12 | Update product with decimal ID | API returns a route error |
| UP13 | Update product with ID containing spaces | API returns a route error |
| UP14 | Update product without name | Original name is retained |
| UP15 | Update product with zero price | Product is updated with zero price |
| UP16 | Update product without price | Original price is retained |

**Result:** 16 passed.

### 3.3 Add to Cart

**Test File:** `tests/test_add_to_cart.py`

**Objective:** Verify that the Store API can add products to the shopping cart and handle invalid product IDs, quantities, and missing request headers.

| Test Case | Description | Expected Result |
|---|---|---|
| AC01 | Add a valid product to cart | Product is added successfully |
| AC02 | Add a non-existing product to cart | API returns an invalid product error |
| AC03 | Add a product using a non-numeric ID | API returns an invalid product error |
| AC04 | Add a non-purchasable product to cart | API returns a product not purchasable error |
| AC05 | Add a product with zero quantity | API returns an invalid quantity error |
| AC06 | Add a product with negative quantity | API returns an invalid quantity error |
| AC07 | Add a product with non-numeric quantity | API returns an invalid parameter error |
| AC08 | Add a product without specifying quantity | Product is added with the default quantity |
| AC09 | Add a product without the Nonce header | API returns a missing Nonce error |

**Result:** 9 passed.

## 4. Overall Test Results

All three API test suites were executed together using the following command:

```powershell
python -m pytest tests -v
```

The test execution completed successfully.

| Test Suite | Total Tests | Passed | Failed |
|---|---:|---:|---:|
| Create Product | 9 | 9 | 0 |
| Update Product | 16 | 16 | 0 |
| Add to Cart | 9 | 9 | 0 |
| **Total** | **34** | **34** | **0** |

**Execution Time:** 10.85 seconds

**Overall Result:** 34 passed, 0 failed.

## 5. Conclusion

The API testing successfully verified three major operations: Create Product, Update Product, and Add to Cart.

A total of **34 test cases** were executed, and all test cases passed. The tests covered valid inputs, invalid inputs, boundary values, omitted fields, and missing request headers.

The results indicate that the API responses matched the expected results defined in the test cases during this test execution.

![alt text](image.png)