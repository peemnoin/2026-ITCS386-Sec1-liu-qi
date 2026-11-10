import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://157.85.102.236/shop/wp-json/wc/v3"

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