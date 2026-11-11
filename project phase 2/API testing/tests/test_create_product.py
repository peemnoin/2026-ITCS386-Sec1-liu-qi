import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://157.85.102.236/shop/wp-json/wc/v3"
ADMIN_API_URL = "http://157.85.102.236/shop/wp-json/wc/v3"

USERNAME = os.getenv("WC_API_USERNAME")
PASSWORD = os.getenv("WC_API_PASSWORD")



def test_create_product_success():
    """CP01: Create a simple product with valid data."""

    assert USERNAME, "Missing WC_API_USERNAME in .env"
    assert PASSWORD, "Missing WC_API_PASSWORD in .env"

    product_data = {
        "name": "G01 Test Product CP01",
        "type": "simple",
        "regular_price": "199"
    }

    response = requests.post(
        f"{BASE_URL}/products",
        auth=(USERNAME, PASSWORD),
        json=product_data,
        timeout=30
    )

    assert response.status_code == 201

    result = response.json()

    assert result["name"] == product_data["name"]
    assert result["type"] == "simple"
    assert result["regular_price"] == "199"
    assert "id" in result

def test_create_product_invalid_type():
    """CP02: Reject product creation with an invalid product type."""

    product_data = {
        "name": "G01 Test Product CP02",
        "type": "invalid_type",
        "regular_price": "199"
    }

    response = requests.post(
        f"{BASE_URL}/products",
        auth=(USERNAME, PASSWORD),
        json=product_data,
        timeout=30
    )

    assert response.status_code == 400

    result = response.json()

    assert "message" in result

def test_create_product_zero_price():
    """CP03: Create a product with zero price."""

    product_data = {
        "name": "G01 Test Product CP03",
        "type": "simple",
        "regular_price": "0"
    }

    response = requests.post(
        f"{BASE_URL}/products",
        auth=(USERNAME, PASSWORD),
        json=product_data,
        timeout=30
    )

    assert response.status_code == 201

    result = response.json()

    assert result["name"] == product_data["name"]
    assert result["type"] == "simple"
    assert result["regular_price"] == "0"
    assert result["price"] == "0"
    assert result["purchasable"] is True
    assert "id" in result

def test_create_product_negative_price():
    """CP04: Create a product with a negative price."""

    product_data = {
        "name": "G01 Test Product CP04",
        "type": "simple",
        "regular_price": "-100"
    }

    response = requests.post(
        f"{BASE_URL}/products",
        auth=(USERNAME, PASSWORD),
        json=product_data,
        timeout=30
    )

    assert response.status_code == 201

    result = response.json()

    assert result["name"] == product_data["name"]
    assert result["type"] == "simple"
    assert result["regular_price"] == "-100"
    assert result["price"] == "-100"
    assert result["purchasable"] is True
    assert "id" in result

def test_create_product_empty_price():
    """CP05: Create a product with an empty price."""

    product_data = {
        "name": "G01 Test Product CP05",
        "type": "simple",
        "regular_price": ""
    }

    response = requests.post(
        f"{BASE_URL}/products",
        auth=(USERNAME, PASSWORD),
        json=product_data,
        timeout=30
    )

    assert response.status_code == 201

    result = response.json()

    assert result["name"] == product_data["name"]
    assert result["type"] == "simple"
    assert result["regular_price"] == ""
    assert result["price"] == ""
    assert result["purchasable"] is False
    assert "id" in result

def test_create_product_non_numeric_price():
    """CP06: Create a product with a non-numeric price."""

    product_data = {
        "name": "G01 Test Product CP06",
        "type": "simple",
        "regular_price": "abc"
    }

    response = requests.post(
        f"{BASE_URL}/products",
        auth=(USERNAME, PASSWORD),
        json=product_data,
        timeout=30
    )

    assert response.status_code == 201

    result = response.json()

    assert result["name"] == product_data["name"]
    assert result["type"] == "simple"
    assert result["regular_price"] == ""
    assert result["price"] == ""
    assert result["purchasable"] is False
    assert "id" in result

def test_create_product_without_price():
    """CP07: Create a product without a price field."""

    product_data = {
        "name": "G01 Test Product CP07",
        "type": "simple"
    }

    response = requests.post(
        f"{BASE_URL}/products",
        auth=(USERNAME, PASSWORD),
        json=product_data,
        timeout=30
    )

    assert response.status_code == 201

    result = response.json()

    assert result["name"] == product_data["name"]
    assert result["type"] == "simple"
    assert result["regular_price"] == ""
    assert result["price"] == ""
    assert result["purchasable"] is False
    assert "id" in result

def test_create_product_without_name():
    """CP08: Create a product without a name field."""

    product_data = {
        "type": "simple",
        "regular_price": "199"
    }

    response = requests.post(
        f"{BASE_URL}/products",
        auth=(USERNAME, PASSWORD),
        json=product_data,
        timeout=30
    )

    assert response.status_code == 201

    result = response.json()

    assert result["name"] == "Product"
    assert result["type"] == "simple"
    assert result["regular_price"] == "199"
    assert result["price"] == "199"
    assert result["purchasable"] is True
    assert "id" in result

def test_create_product_empty_name():
    """CP09: Create a product with an empty name."""

    product_data = {
        "name": "",
        "type": "simple",
        "regular_price": "199"
    }

    response = requests.post(
        f"{BASE_URL}/products",
        auth=(USERNAME, PASSWORD),
        json=product_data,
        timeout=30
    )

    assert response.status_code == 201

    result = response.json()

    assert result["name"] == "Product"
    assert result["type"] == "simple"
    assert result["regular_price"] == "199"
    assert result["price"] == "199"
    assert result["purchasable"] is True
    assert "id" in result