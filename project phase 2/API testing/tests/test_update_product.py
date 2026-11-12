"""Test suite for the Update Product operation.

Endpoint: PUT /wp-json/wc/v3/products/{id}
Test inputs come from Input Space Partitioning (see README section 3.2.2).

Each test creates its own product through the `product` fixture, which is
deleted automatically when the test ends. Expected results follow how a
shop SHOULD behave; where the API behaves differently the test fails and
is analysed as a defect (UP05, UP07).
"""

import pytest

REQUEST_TIMEOUT = 30  # seconds


@pytest.fixture
def product(post_product):
    """Create a fresh product (price 199) owned by the current test."""
    response = post_product(
        {
            "name": "G01 Test Product UP",
            "type": "simple",
            "regular_price": "199",
        }
    )
    assert response.status_code == 201, (
        f"Test setup failed: could not create product ({response.text})"
    )
    return response.json()


@pytest.fixture
def put_product(admin_api, admin_url):
    """Return a function that sends PUT /products/{id}."""

    def _put_product(product_id, payload):
        return admin_api.put(
            f"{admin_url}/products/{product_id}",
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )

    return _put_product


def test_update_product_success(product, put_product):
    """UP01: Update an existing product with a valid name and price."""
    payload = {"name": "G01 Updated Product UP01", "regular_price": "299"}

    response = put_product(product["id"], payload)

    assert response.status_code == 200, response.text
    result = response.json()
    assert result["id"] == product["id"]
    assert result["name"] == payload["name"]
    assert result["regular_price"] == "299"
    assert result["price"] == "299"
    assert result["purchasable"] is True


def test_update_product_non_existing_id(put_product):
    """UP02: Reject an update for a product ID that does not exist."""
    response = put_product(99999999, {"regular_price": "299"})

    assert response.status_code == 400, response.text
    result = response.json()
    assert result["code"] == "woocommerce_rest_product_invalid_id"
    assert result["data"]["status"] == 400


def test_update_product_non_numeric_id(put_product):
    """UP03: A non-numeric ID matches no route, so the API returns 404."""
    response = put_product("abc", {"regular_price": "299"})

    assert response.status_code == 404, response.text
    result = response.json()
    assert result["code"] == "rest_no_route"
    assert result["data"]["status"] == 404


def test_update_product_empty_name(product, put_product):
    """UP04: An empty name is ignored and the original name is kept."""
    response = put_product(product["id"], {"name": "", "regular_price": "299"})

    assert response.status_code == 200, response.text
    result = response.json()
    assert result["id"] == product["id"]
    assert result["name"] == product["name"]
    assert result["regular_price"] == "299"


def test_update_product_negative_price(product, put_product):
    """UP05: Reject a negative price. A shop must not sell at a negative price."""
    response = put_product(product["id"], {"regular_price": "-100"})

    assert response.status_code == 400, (
        f"Expected 400 for negative price but got {response.status_code}: "
        f"{response.text}"
    )
    assert "message" in response.json()


def test_update_product_empty_price(product, put_product):
    """UP06: An empty price is accepted, but the product is not purchasable."""
    response = put_product(product["id"], {"regular_price": ""})

    assert response.status_code == 200, response.text
    result = response.json()
    assert result["id"] == product["id"]
    assert result["regular_price"] == ""
    assert result["price"] == ""
    assert result["purchasable"] is False



def test_update_product_non_numeric_price(
    product, put_product, admin_api, admin_url
):
    """UP07: Reject a non-numeric price and retain the original price."""
    response = put_product(product["id"], {"regular_price": "abc"})

    assert response.status_code == 400, (
        f"Expected 400 for non-numeric price but got {response.status_code}: "
        f"{response.text}"
    )
    assert "message" in response.json()

    # Verify that the original product price remains unchanged.
    check_response = admin_api.get(
        f"{admin_url}/products/{product['id']}",
        timeout=REQUEST_TIMEOUT
    )

    assert check_response.status_code == 200, check_response.text

    result = check_response.json()
    assert result["regular_price"] == "199"
    assert result["price"] == "199"
    assert result["purchasable"] is True



def test_update_product_empty_body(product, put_product):
    """UP08: An empty request body changes nothing."""
    response = put_product(product["id"], {})

    assert response.status_code == 200, response.text
    result = response.json()
    assert result["id"] == product["id"]
    assert result["name"] == product["name"]
    assert result["regular_price"] == "199"
    assert result["price"] == "199"
    assert result["purchasable"] is True


def test_update_product_zero_id(put_product):
    """UP09: Reject product ID 0 (boundary value)."""
    response = put_product(0, {"regular_price": "299"})

    assert response.status_code == 400, response.text
    result = response.json()
    assert result["code"] == "woocommerce_rest_product_invalid_id"
    assert result["data"]["status"] == 400


def test_update_product_negative_id(put_product):
    """UP10: A negative ID matches no route, so the API returns 404."""
    response = put_product(-1, {"regular_price": "299"})

    assert response.status_code == 404, response.text
    result = response.json()
    assert result["code"] == "rest_no_route"
    assert result["data"]["status"] == 404


def test_update_product_without_name(product, put_product):
    """UP11: Omitting the name keeps the original name."""
    response = put_product(product["id"], {"regular_price": "299"})

    assert response.status_code == 200, response.text
    result = response.json()
    assert result["name"] == product["name"]
    assert result["regular_price"] == "299"
    assert result["price"] == "299"
    assert result["purchasable"] is True


def test_update_product_zero_price(product, put_product):
    """UP12: Accept a zero price (boundary value)."""
    response = put_product(product["id"], {"regular_price": "0"})

    assert response.status_code == 200, response.text
    result = response.json()
    assert result["regular_price"] == "0"
    assert result["price"] == "0"
    assert result["purchasable"] is True


def test_update_product_without_price(product, put_product):
    """UP13: Omitting the price keeps the original price."""
    response = put_product(product["id"], {"name": "G01 Updated Product UP13"})

    assert response.status_code == 200, response.text
    result = response.json()
    assert result["name"] == "G01 Updated Product UP13"
    assert result["regular_price"] == "199"
    assert result["price"] == "199"
    assert result["purchasable"] is True
