
# API Testing Results

## 1. Overview
This test suite verifies three WooCommerce API operations:
- Create Product
- Update Product
- Add Item to Cart
Testing was implemented using Python, pytest, and requests.

## 2. Test Cases

| Test ID | API Operation | Test Scenario | Expected Result |
|---|---|---|---|
| CP01 | Create Product | Create a product with valid data | HTTP 201 Created |
| CP02 | Create Product | Create a product with an invalid product type | HTTP 400 Bad Request |
| UP01 | Update Product | Update an existing product with valid data | HTTP 200 OK |
| AC01 | Add Item to Cart | Add a purchasable product to the cart | HTTP 201 Created |

## 3. Execution Results
Command:
```bash
python -m pytest -v
```
Result:
- Total test cases: 4
- Passed: 4
- Failed: 0
- Execution time: 1.34 seconds

## 4. Summary
All four API test cases passed successfully.

The tests verified product creation, invalid product type handling, product updates, and adding products to the shopping cart.

![alt text](image.png)