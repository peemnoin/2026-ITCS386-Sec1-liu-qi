import requests

BASE_URL = "http://157.85.102.236/shop/wp-json/wc/store/v1"

response = requests.get(
    f"{BASE_URL}/products",
    params={"per_page": 5},
    timeout=30
)

# Check HTTP status
assert response.status_code == 200

# Check response structure
products = response.json()

assert isinstance(products, list)
assert len(products) > 0

# Check important product fields
for product in products:
    assert "id" in product
    assert "name" in product
    assert "type" in product
    assert "prices" in product

print("API Check: PASSED")
print("Status Code:", response.status_code)
print("Products Retrieved:", len(products))