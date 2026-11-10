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