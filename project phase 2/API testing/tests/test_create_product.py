"""Test suite for the Create Product operation.

Endpoint: POST /wp-json/wc/v3/products
Test inputs come from Input Space Partitioning (see README section 3.2.1).

Expected results follow how a shop SHOULD behave. Where the API behaves
differently, the test fails and is analysed as a defect (CP04, CP06).
"""


def test_create_product_success(post_product):
    """CP01: Create a simple product with valid data."""
    payload = {
        "name": "G01 Test Product CP01",
        "type": "simple",
        "regular_price": "199",
    }

    response = post_product(payload)

    assert response.status_code == 201, response.text
    result = response.json()
    assert result["name"] == payload["name"]
    assert result["type"] == "simple"
    assert result["regular_price"] == "199"
    assert "id" in result


def test_create_product_invalid_type(post_product):
    """CP02: Reject product creation with an invalid product type."""
    payload = {
        "name": "G01 Test Product CP02",
        "type": "invalid_type",
        "regular_price": "199",
    }

    response = post_product(payload)

    assert response.status_code == 400, response.text
    assert "message" in response.json()


def test_create_product_zero_price(post_product):
    """CP03: Accept a product with zero price (boundary value)."""
    payload = {
        "name": "G01 Test Product CP03",
        "type": "simple",
        "regular_price": "0",
    }

    response = post_product(payload)

    assert response.status_code == 201, response.text
    result = response.json()
    assert result["name"] == payload["name"]
    assert result["regular_price"] == "0"
    assert result["price"] == "0"
    assert result["purchasable"] is True


def test_create_product_negative_price(post_product):
    """CP04: Reject a negative price. A shop must not sell at a negative price."""
    payload = {
        "name": "G01 Test Product CP04",
        "type": "simple",
        "regular_price": "-100",
    }

    response = post_product(payload)

    assert response.status_code == 400, (
        f"Expected 400 for negative price but got {response.status_code}: "
        f"{response.text}"
    )
    assert "message" in response.json()


def test_create_product_empty_price(post_product):
    """CP05: Accept an empty price, but the product must not be purchasable."""
    payload = {
        "name": "G01 Test Product CP05",
        "type": "simple",
        "regular_price": "",
    }

    response = post_product(payload)

    assert response.status_code == 201, response.text
    result = response.json()
    assert result["regular_price"] == ""
    assert result["price"] == ""
    assert result["purchasable"] is False


def test_create_product_non_numeric_price(post_product):
    """CP06: Reject a non-numeric price instead of silently dropping it."""
    payload = {
        "name": "G01 Test Product CP06",
        "type": "simple",
        "regular_price": "abc",
    }

    response = post_product(payload)

    assert response.status_code == 400, (
        f"Expected 400 for non-numeric price but got {response.status_code}: "
        f"{response.text}"
    )
    assert "message" in response.json()


def test_create_product_without_price(post_product):
    """CP07: Accept a product with no price field; it is not purchasable."""
    payload = {
        "name": "G01 Test Product CP07",
        "type": "simple",
    }

    response = post_product(payload)

    assert response.status_code == 201, response.text
    result = response.json()
    assert result["name"] == payload["name"]
    assert result["regular_price"] == ""
    assert result["purchasable"] is False


def test_create_product_without_name(post_product):
    """CP08: Product without a name field gets the default name "Product"."""
    payload = {
        "type": "simple",
        "regular_price": "199",
    }

    response = post_product(payload)

    assert response.status_code == 201, response.text
    result = response.json()
    assert result["name"] == "Product"
    assert result["regular_price"] == "199"
    assert result["purchasable"] is True


def test_create_product_empty_name(post_product):
    """CP09: Product with an empty name gets the default name "Product"."""
    payload = {
        "name": "",
        "type": "simple",
        "regular_price": "199",
    }

    response = post_product(payload)

    assert response.status_code == 201, response.text
    result = response.json()
    assert result["name"] == "Product"
    assert result["regular_price"] == "199"
    assert result["purchasable"] is True
