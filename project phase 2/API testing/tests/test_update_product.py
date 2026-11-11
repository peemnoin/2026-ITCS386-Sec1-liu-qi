import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://157.85.102.236/shop/wp-json/wc/v3"

USERNAME = os.getenv("WC_API_USERNAME")
PASSWORD = os.getenv("WC_API_PASSWORD")


def test_update_product_success():
    """UP01: Update an existing product with valid data."""

    assert USERNAME, "Missing WC_API_USERNAME in .env"
    assert PASSWORD, "Missing WC_API_PASSWORD in .env"

    # Create a test product first
    product_data = {
        "name": "G01 Test Product UP01",
        "type": "simple",
        "regular_price": "199"
    }

    create_response = requests.post(
        f"{BASE_URL}/products",
        auth=(USERNAME, PASSWORD),
        json=product_data,
        timeout=30
    )

    assert create_response.status_code == 201

    product_id = create_response.json()["id"]

    # Update the product name and price
    updated_data = {
        "name": "G01 Updated Product UP01",
        "regular_price": "299"
    }

    update_response = requests.put(
        f"{BASE_URL}/products/{product_id}",
        auth=(USERNAME, PASSWORD),
        json=updated_data,
        timeout=30
    )

    assert update_response.status_code == 200

    result = update_response.json()

    assert result["id"] == product_id
    assert result["name"] == updated_data["name"]
    assert result["regular_price"] == "299"
    assert result["price"] == "299"
    assert result["purchasable"] is True


def test_update_product_non_existing_id():
    """UP02: Verify that updating a non-existing product returns an error."""

    assert USERNAME, "Missing WC_API_USERNAME in .env"
    assert PASSWORD, "Missing WC_API_PASSWORD in .env"

    updated_data = {
        "name": "G01 Updated Product UP02",
        "regular_price": "299"
    }

    response = requests.put(
        f"{BASE_URL}/products/99999999",
        auth=(USERNAME, PASSWORD),
        json=updated_data,
        timeout=30
    )

    print("Status Code:", response.status_code)
    print("Response Body:", response.text)

    assert response.status_code == 400

    result = response.json()

    assert result["code"] == "woocommerce_rest_product_invalid_id"
    assert result["message"] == "Invalid ID."
    assert result["data"]["status"] == 400


def test_update_product_invalid_id():
    """UP03: Verify that updating a product with a non-numeric ID returns an error."""

    assert USERNAME, "Missing WC_API_USERNAME in .env"
    assert PASSWORD, "Missing WC_API_PASSWORD in .env"

    updated_data = {
        "name": "G01 Updated Product UP03",
        "regular_price": "299"
    }

    response = requests.put(
        f"{BASE_URL}/products/abc",
        auth=(USERNAME, PASSWORD),
        json=updated_data,
        timeout=30
    )

    print("Status Code:", response.status_code)
    print("Response Body:", response.text)

    assert response.status_code == 404

    result = response.json()

    assert result["code"] == "rest_no_route"
    assert result["message"] == "No route was found matching the URL and request method."
    assert result["data"]["status"] == 404


def test_update_product_empty_name():
    """UP04: Verify API behavior when updating a product with an empty name."""

    assert USERNAME, "Missing WC_API_USERNAME in .env"
    assert PASSWORD, "Missing WC_API_PASSWORD in .env"

    # Create an independent test product
    product_data = {
        "name": "G01 Test Product UP04",
        "type": "simple",
        "regular_price": "199"
    }

    create_response = requests.post(
        f"{BASE_URL}/products",
        auth=(USERNAME, PASSWORD),
        json=product_data,
        timeout=30
    )

    assert create_response.status_code == 201
    product_id = create_response.json()["id"]

    # Update product with an empty name
    updated_data = {
        "name": "",
        "regular_price": "299"
    }

    response = requests.put(
        f"{BASE_URL}/products/{product_id}",
        auth=(USERNAME, PASSWORD),
        json=updated_data,
        timeout=30
    )

    print("Status Code:", response.status_code)
    print("Response Body:", response.text)

    assert response.status_code == 200
    result = response.json()

    assert result["id"] == product_id
    assert result["name"] == product_data["name"]
    assert result["regular_price"] == "299"

def test_update_product_negative_price():
    """UP05: Verify API behavior when updating a product with a negative price."""

    assert USERNAME, "Missing WC_API_USERNAME in .env"
    assert PASSWORD, "Missing WC_API_PASSWORD in .env"

    # Create an independent test product
    product_data = {
        "name": "G01 Test Product UP05",
        "type": "simple",
        "regular_price": "199"
    }

    create_response = requests.post(
        f"{BASE_URL}/products",
        auth=(USERNAME, PASSWORD),
        json=product_data,
        timeout=30
    )

    assert create_response.status_code == 201
    product_id = create_response.json()["id"]

    # Update product with a negative price
    updated_data = {
        "regular_price": "-100"
    }

    response = requests.put(
        f"{BASE_URL}/products/{product_id}",
        auth=(USERNAME, PASSWORD),
        json=updated_data,
        timeout=30
    )

    print("Status Code:", response.status_code)
    print("Response Body:", response.text)

    assert response.status_code == 200

    result = response.json()

    assert result["id"] == product_id
    assert result["regular_price"] == "-100"
    assert result["price"] == "-100"

def test_update_product_empty_price():
    """UP06: Verify API behavior when updating a product with an empty price."""

    assert USERNAME, "Missing WC_API_USERNAME in .env"
    assert PASSWORD, "Missing WC_API_PASSWORD in .env"

    # Create an independent test product
    product_data = {
        "name": "G01 Test Product UP06",
        "type": "simple",
        "regular_price": "199"
    }

    create_response = requests.post(
        f"{BASE_URL}/products",
        auth=(USERNAME, PASSWORD),
        json=product_data,
        timeout=30
    )

    assert create_response.status_code == 201
    product_id = create_response.json()["id"]

    # Update product with an empty price
    updated_data = {
        "regular_price": ""
    }

    response = requests.put(
        f"{BASE_URL}/products/{product_id}",
        auth=(USERNAME, PASSWORD),
        json=updated_data,
        timeout=30
    )

    print("Status Code:", response.status_code)
    print("Response Body:", response.text)

    assert response.status_code == 200

    result = response.json()

    assert result["id"] == product_id
    assert result["regular_price"] == ""
    assert result["price"] == ""
    assert result["purchasable"] is False

def test_update_product_non_numeric_price():
    """UP07: Verify API behavior when updating a product with a non-numeric price."""

    assert USERNAME, "Missing WC_API_USERNAME in .env"
    assert PASSWORD, "Missing WC_API_PASSWORD in .env"

    # Create an independent test product
    product_data = {
        "name": "G01 Test Product UP07",
        "type": "simple",
        "regular_price": "199"
    }

    create_response = requests.post(
        f"{BASE_URL}/products",
        auth=(USERNAME, PASSWORD),
        json=product_data,
        timeout=30
    )

    assert create_response.status_code == 201
    product_id = create_response.json()["id"]

    # Update product with a non-numeric price
    updated_data = {
        "regular_price": "abc"
    }

    response = requests.put(
        f"{BASE_URL}/products/{product_id}",
        auth=(USERNAME, PASSWORD),
        json=updated_data,
        timeout=30
    )

    print("Status Code:", response.status_code)
    print("Response Body:", response.text)

    assert response.status_code == 200

    result = response.json()

    assert result["id"] == product_id
    assert result["regular_price"] == ""
    assert result["price"] == ""
    assert result["purchasable"] is False

def test_update_product_empty_body():
    """UP08: Verify API behavior when updating a product with an empty request body."""

    assert USERNAME, "Missing WC_API_USERNAME in .env"
    assert PASSWORD, "Missing WC_API_PASSWORD in .env"

    # Create an independent test product
    product_data = {
        "name": "G01 Test Product UP08",
        "type": "simple",
        "regular_price": "199"
    }

    create_response = requests.post(
        f"{BASE_URL}/products",
        auth=(USERNAME, PASSWORD),
        json=product_data,
        timeout=30
    )

    assert create_response.status_code == 201
    product_id = create_response.json()["id"]

    # Update product with an empty request body
    response = requests.put(
        f"{BASE_URL}/products/{product_id}",
        auth=(USERNAME, PASSWORD),
        json={},
        timeout=30
    )

    print("Status Code:", response.status_code)
    print("Response Body:", response.text)

    assert response.status_code == 200

    result = response.json()

    assert result["id"] == product_id
    assert result["name"] == product_data["name"]
    assert result["regular_price"] == "199"
    assert result["price"] == "199"
    assert result["purchasable"] is True

def test_update_product_zero_id():
    """UP09: Verify that updating a product with ID zero returns an error."""

    assert USERNAME, "Missing WC_API_USERNAME in .env"
    assert PASSWORD, "Missing WC_API_PASSWORD in .env"

    updated_data = {
        "name": "G01 Updated Product UP09",
        "regular_price": "299"
    }

    response = requests.put(
        f"{BASE_URL}/products/0",
        auth=(USERNAME, PASSWORD),
        json=updated_data,
        timeout=30
    )

    print("Status Code:", response.status_code)
    print("Response Body:", response.text)

    assert response.status_code == 400

    result = response.json()

    assert result["code"] == "woocommerce_rest_product_invalid_id"
    assert result["message"] == "Invalid ID."
    assert result["data"]["status"] == 400

def test_update_product_negative_id():
    """UP10: Verify that updating a product with a negative ID returns an error."""

    assert USERNAME, "Missing WC_API_USERNAME in .env"
    assert PASSWORD, "Missing WC_API_PASSWORD in .env"

    updated_data = {
        "name": "G01 Updated Product UP10",
        "regular_price": "299"
    }

    response = requests.put(
        f"{BASE_URL}/products/-1",
        auth=(USERNAME, PASSWORD),
        json=updated_data,
        timeout=30
    )

    print("Status Code:", response.status_code)
    print("Response Body:", response.text)

    assert response.status_code == 404

    result = response.json()

    assert result["code"] == "rest_no_route"
    assert result["message"] == "No route was found matching the URL and request method."
    assert result["data"]["status"] == 404

def test_update_product_alphanumeric_id():
    """UP11: Verify that updating a product with an alphanumeric ID returns an error."""

    assert USERNAME, "Missing WC_API_USERNAME in .env"
    assert PASSWORD, "Missing WC_API_PASSWORD in .env"

    updated_data = {
        "name": "G01 Updated Product UP11",
        "regular_price": "299"
    }

    response = requests.put(
        f"{BASE_URL}/products/123abc",
        auth=(USERNAME, PASSWORD),
        json=updated_data,
        timeout=30
    )

    print("Status Code:", response.status_code)
    print("Response Body:", response.text)

    assert response.status_code == 404

    result = response.json()

    assert result["code"] == "rest_no_route"
    assert result["message"] == "No route was found matching the URL and request method."
    assert result["data"]["status"] == 404

def test_update_product_decimal_id():
    """UP12: Verify API behavior when updating a product with a decimal ID."""

    assert USERNAME, "Missing WC_API_USERNAME in .env"
    assert PASSWORD, "Missing WC_API_PASSWORD in .env"

    updated_data = {
        "name": "G01 Updated Product UP12",
        "regular_price": "299"
    }

    response = requests.put(
        f"{BASE_URL}/products/1.5",
        auth=(USERNAME, PASSWORD),
        json=updated_data,
        timeout=30
    )

    print("Status Code:", response.status_code)
    print("Response Body:", response.text)

    assert response.status_code == 404

    result = response.json()

    assert result["code"] == "rest_no_route"
    assert result["message"] == "No route was found matching the URL and request method."
    assert result["data"]["status"] == 404

def test_update_product_id_with_spaces():
    """UP13: Verify API behavior when updating a product with spaces in the ID."""

    assert USERNAME, "Missing WC_API_USERNAME in .env"
    assert PASSWORD, "Missing WC_API_PASSWORD in .env"

    updated_data = {
        "name": "G01 Updated Product UP13",
        "regular_price": "299"
    }

    response = requests.put(
        f"{BASE_URL}/products/%20123%20",
        auth=(USERNAME, PASSWORD),
        json=updated_data,
        timeout=30
    )

    print("Status Code:", response.status_code)
    print("Response Body:", response.text)

    assert response.status_code == 404

    result = response.json()

    assert result["code"] == "rest_no_route"
    assert result["message"] == "No route was found matching the URL and request method."
    assert result["data"]["status"] == 404

def test_update_product_without_name():
    """UP14: Verify that updating a product without a name field preserves the original name."""

    assert USERNAME, "Missing WC_API_USERNAME in .env"
    assert PASSWORD, "Missing WC_API_PASSWORD in .env"

    # Create an independent test product
    product_data = {
        "name": "G01 Test Product UP14",
        "type": "simple",
        "regular_price": "199"
    }

    create_response = requests.post(
        f"{BASE_URL}/products",
        auth=(USERNAME, PASSWORD),
        json=product_data,
        timeout=30
    )

    assert create_response.status_code == 201
    product_id = create_response.json()["id"]

    # Update product without the name field
    updated_data = {
        "regular_price": "299"
    }

    response = requests.put(
        f"{BASE_URL}/products/{product_id}",
        auth=(USERNAME, PASSWORD),
        json=updated_data,
        timeout=30
    )

    print("Status Code:", response.status_code)
    print("Response Body:", response.text)

    assert response.status_code == 200

    result = response.json()

    assert result["id"] == product_id
    assert result["name"] == product_data["name"]
    assert result["regular_price"] == "299"
    assert result["price"] == "299"
    assert result["purchasable"] is True

def test_update_product_zero_price():
    """UP15: Verify API behavior when updating a product with zero price."""

    assert USERNAME, "Missing WC_API_USERNAME in .env"
    assert PASSWORD, "Missing WC_API_PASSWORD in .env"

    # Create an independent test product
    product_data = {
        "name": "G01 Test Product UP15",
        "type": "simple",
        "regular_price": "199"
    }

    create_response = requests.post(
        f"{BASE_URL}/products",
        auth=(USERNAME, PASSWORD),
        json=product_data,
        timeout=30
    )

    assert create_response.status_code == 201
    product_id = create_response.json()["id"]

    # Update product with zero price
    updated_data = {
        "regular_price": "0"
    }

    response = requests.put(
        f"{BASE_URL}/products/{product_id}",
        auth=(USERNAME, PASSWORD),
        json=updated_data,
        timeout=30
    )

    print("Status Code:", response.status_code)
    print("Response Body:", response.text)

    assert response.status_code == 200

    result = response.json()

    assert result["id"] == product_id
    assert result["regular_price"] == "0"
    assert result["price"] == "0"
    assert result["purchasable"] is True

def test_update_product_without_price():
    """UP16: Verify that updating a product without a price field preserves the original price."""

    assert USERNAME, "Missing WC_API_USERNAME in .env"
    assert PASSWORD, "Missing WC_API_PASSWORD in .env"

    # Create an independent test product
    product_data = {
        "name": "G01 Test Product UP16",
        "type": "simple",
        "regular_price": "199"
    }

    create_response = requests.post(
        f"{BASE_URL}/products",
        auth=(USERNAME, PASSWORD),
        json=product_data,
        timeout=30
    )

    assert create_response.status_code == 201
    product_id = create_response.json()["id"]

    # Update product without the regular_price field
    updated_data = {
        "name": "G01 Updated Product UP16"
    }

    response = requests.put(
        f"{BASE_URL}/products/{product_id}",
        auth=(USERNAME, PASSWORD),
        json=updated_data,
        timeout=30
    )

    print("Status Code:", response.status_code)
    print("Response Body:", response.text)

    assert response.status_code == 200

    result = response.json()

    assert result["id"] == product_id
    assert result["name"] == updated_data["name"]
    assert result["regular_price"] == "199"
    assert result["price"] == "199"
    assert result["purchasable"] is True