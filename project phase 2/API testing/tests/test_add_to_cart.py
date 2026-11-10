
import requests

BASE_URL = "http://157.85.102.236/shop/wp-json/wc/store/v1"


def test_add_item_to_cart():
    """AC01: Add a purchasable product to the cart."""

    session = requests.Session()

    # Step 1: Get available products
    products_response = session.get(
        f"{BASE_URL}/products",
        params={"per_page": 20},
        timeout=30
    )

    assert products_response.status_code == 200

    products = products_response.json()

    # Find a purchasable product that is in stock
    purchasable_products = [
        product for product in products
        if product.get("is_purchasable")
        and product.get("is_in_stock")
    ]

    assert len(purchasable_products) > 0

    product_id = purchasable_products[0]["id"]

    # Step 2: Initialize cart session
    cart_response = session.get(
        f"{BASE_URL}/cart",
        timeout=30
    )

    assert cart_response.status_code == 200

    # Extract Cart Token and Nonce if provided
    cart_token = cart_response.headers.get("Cart-Token")
    nonce = cart_response.headers.get("Nonce")

    print("Cart Response Headers:", dict(cart_response.headers))
    print("Cart Token Available:", bool(cart_token))
    print("Nonce Available:", bool(nonce))

    # Step 3: Prepare request headers
    headers = {}

    if cart_token:
        headers["Cart-Token"] = cart_token

    if nonce:
        headers["Nonce"] = nonce

    # Step 4: Add product to cart
    add_response = session.post(
        f"{BASE_URL}/cart/add-item",
        headers=headers,
        data={
            "id": product_id,
            "quantity": 1
        },
        timeout=30
    )

    print("Add Cart Status:", add_response.status_code)
    print("Add Cart Response:", add_response.text)
    print("Add Cart Headers:", dict(add_response.headers))

    # Step 5: Verify response
    assert add_response.status_code == 201, (
        f"Expected 201 but received {add_response.status_code}: "
        f"{add_response.text}"
    )

    result = add_response.json()

    assert "items" in result

    assert any(
        item["id"] == product_id
        for item in result["items"]
    )
