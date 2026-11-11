
import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://157.85.102.236/shop/wp-json/wc/store/v1"
ADMIN_API_URL = "http://157.85.102.236/shop/wp-json/wc/v3"

USERNAME = os.getenv("WC_API_USERNAME")
PASSWORD = os.getenv("WC_API_PASSWORD")


def create_test_product(name, price="199"):
    """Create a product owned by this test case."""

    assert USERNAME, "Missing WC_API_USERNAME in .env"
    assert PASSWORD, "Missing WC_API_PASSWORD in .env"

    response = requests.post(
        f"{ADMIN_API_URL}/products",
        auth=(USERNAME, PASSWORD),
        json={
            "name": name,
            "type": "simple",
            "regular_price": price
        },
        timeout=30
    )

    assert response.status_code == 201, (
        f"Product creation failed: HTTP {response.status_code}"
    )

    return response.json()["id"]


def delete_test_product(product_id):
    """Delete only the product created by this test case."""

    response = requests.delete(
        f"{ADMIN_API_URL}/products/{product_id}",
        auth=(USERNAME, PASSWORD),
        params={"force": True},
        timeout=30
    )

    assert response.status_code == 200, (
        f"Product deletion failed: HTTP {response.status_code}"
    )


def get_cart_headers(session):
    """Initialize a cart session and retrieve its request headers."""

    response = session.get(
        f"{BASE_URL}/cart",
        timeout=30
    )

    assert response.status_code == 200

    headers = {}

    cart_token = response.headers.get("Cart-Token")
    nonce = response.headers.get("Nonce")

    if cart_token:
        headers["Cart-Token"] = cart_token

    if nonce:
        headers["Nonce"] = nonce

    return headers


def test_add_item_to_cart():
    """AC01: Add a purchasable product to the cart."""

    product_id = create_test_product("G01 API Cart AC01")

    try:
        session = requests.Session()
        headers = get_cart_headers(session)

        response = session.post(
            f"{BASE_URL}/cart/add-item",
            headers=headers,
            data={"id": product_id, "quantity": 1},
            timeout=30
        )

        assert response.status_code == 201

        result = response.json()

        assert "items" in result
        assert any(
            item["id"] == product_id and item["quantity"] == 1
            for item in result["items"]
        )

    finally:
        delete_test_product(product_id)


def test_add_non_existing_product_to_cart():
    """AC02: Verify that a non-existing product cannot be added to the cart."""

    session = requests.Session()
    headers = get_cart_headers(session)

    response = session.post(
        f"{BASE_URL}/cart/add-item",
        headers=headers,
        data={"id": 99999999, "quantity": 1},
        timeout=30
    )

    assert response.status_code == 400

    result = response.json()

    assert result["code"] == "woocommerce_rest_cart_invalid_product"
    assert result["data"]["status"] == 400
    assert "99999999" in result["message"]


def test_add_invalid_product_id_to_cart():
    """AC03: Verify that a non-numeric product ID cannot be added to the cart."""

    session = requests.Session()
    headers = get_cart_headers(session)

    response = session.post(
        f"{BASE_URL}/cart/add-item",
        headers=headers,
        data={"id": "abc", "quantity": 1},
        timeout=30
    )

    assert response.status_code == 400

    result = response.json()

    assert result["code"] == "woocommerce_rest_cart_invalid_product"
    assert result["data"]["status"] == 400
    assert "&quot;0&quot;" in result["message"]


def test_add_non_purchasable_product_to_cart():
    """AC04: Verify that a non-purchasable product cannot be added to the cart."""

    product_id = create_test_product("G01 API Cart AC04", price="")

    try:
        session = requests.Session()
        headers = get_cart_headers(session)

        response = session.post(
            f"{BASE_URL}/cart/add-item",
            headers=headers,
            data={"id": product_id, "quantity": 1},
            timeout=30
        )

        assert response.status_code == 400

        result = response.json()

        assert result["code"] == "woocommerce_rest_product_not_purchasable"
        assert result["data"]["status"] == 400
        assert "not available for purchase" in result["message"]

    finally:
        delete_test_product(product_id)


def test_add_zero_quantity_to_cart():
    """AC05: Verify that zero quantity cannot be added to the cart."""

    product_id = create_test_product("G01 API Cart AC05")

    try:
        session = requests.Session()
        headers = get_cart_headers(session)

        response = session.post(
            f"{BASE_URL}/cart/add-item",
            headers=headers,
            data={"id": product_id, "quantity": 0},
            timeout=30
        )

        assert response.status_code == 400

        result = response.json()

        assert result["code"] == "woocommerce_rest_product_invalid_quantity"
        assert result["data"]["status"] == 400
        assert "less than or equal to 0" in result["message"]

    finally:
        delete_test_product(product_id)


def test_add_negative_quantity_to_cart():
    """AC06: Verify that negative quantity cannot be added to the cart."""

    product_id = create_test_product("G01 API Cart AC06")

    try:
        session = requests.Session()
        headers = get_cart_headers(session)

        response = session.post(
            f"{BASE_URL}/cart/add-item",
            headers=headers,
            data={"id": product_id, "quantity": -1},
            timeout=30
        )

        assert response.status_code == 400

        result = response.json()

        assert result["code"] == "woocommerce_rest_product_invalid_quantity"
        assert result["data"]["status"] == 400
        assert "less than or equal to 0" in result["message"]

    finally:
        delete_test_product(product_id)


def test_add_non_numeric_quantity_to_cart():
    """AC07: Verify that non-numeric quantity is rejected."""

    product_id = create_test_product("G01 API Cart AC07")

    try:
        session = requests.Session()
        headers = get_cart_headers(session)

        response = session.post(
            f"{BASE_URL}/cart/add-item",
            headers=headers,
            data={"id": product_id, "quantity": "abc"},
            timeout=30
        )

        assert response.status_code == 400

        result = response.json()

        assert result["code"] == "rest_invalid_param"
        assert result["data"]["status"] == 400
        assert "quantity" in result["data"]["params"]
        assert (
            result["data"]["params"]["quantity"]
            == "quantity is not of type number."
        )

    finally:
        delete_test_product(product_id)


def test_add_item_without_quantity_to_cart():
    """AC08: Verify that omitted quantity defaults to one."""

    product_id = create_test_product("G01 API Cart AC08")

    try:
        session = requests.Session()
        headers = get_cart_headers(session)

        response = session.post(
            f"{BASE_URL}/cart/add-item",
            headers=headers,
            data={"id": product_id},
            timeout=30
        )

        assert response.status_code == 201

        result = response.json()

        assert "items" in result
        assert any(
            item["id"] == product_id and item["quantity"] == 1
            for item in result["items"]
        )

    finally:
        delete_test_product(product_id)


def test_add_item_without_nonce():
    """AC09: Verify that adding an item without a nonce is rejected."""

    response = requests.post(
        f"{BASE_URL}/cart/add-item",
        data={
            "id": 99999999,
            "quantity": 1
        },
        timeout=30
    )

    assert response.status_code == 401

    result = response.json()

    assert result["code"] == "woocommerce_rest_missing_nonce"
    assert result["data"]["status"] == 401
    assert "Missing the Nonce header" in result["message"]
