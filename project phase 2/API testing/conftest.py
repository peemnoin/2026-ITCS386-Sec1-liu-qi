"""Shared fixtures for the WooCommerce API test suites.

Fixtures defined here are discovered automatically by pytest.
They handle login, product creation and cleanup, so each test file
stays short and every test remains independent.
"""

import os

import pytest
import requests
from dotenv import load_dotenv

# Read WC_API_USERNAME and WC_API_PASSWORD from the local .env file.
load_dotenv()

ADMIN_API_URL = "http://157.85.102.236/shop/wp-json/wc/v3"
REQUEST_TIMEOUT = 30  # seconds


@pytest.fixture(scope="session")
def admin_url():
    """Base URL of the Admin REST API."""
    return ADMIN_API_URL


@pytest.fixture(scope="session")
def admin_api():
    """A requests session that sends the group's Basic Auth on every call.

    Stops the whole run with a clear message if credentials are missing,
    instead of failing later with confusing 401 errors.
    """
    username = os.getenv("WC_API_USERNAME")
    password = os.getenv("WC_API_PASSWORD")

    if not username or not password:
        pytest.fail(
            "Missing WC_API_USERNAME or WC_API_PASSWORD. "
            "Create a .env file (see .env.example)."
        )

    session = requests.Session()
    session.auth = (username, password)
    return session


@pytest.fixture
def product_cleanup(admin_api, admin_url):
    """A list of product IDs created by ONE test.

    Test code appends IDs to this list. After the test finishes (pass or
    fail), every ID in the list is deleted. Only IDs that this test
    created are ever deleted, so demo data and other groups' data are
    never touched.
    """
    created_ids = []

    yield created_ids  # the test runs here

    for product_id in created_ids:
        response = admin_api.delete(
            f"{admin_url}/products/{product_id}",
            params={"force": True},
            timeout=REQUEST_TIMEOUT,
        )
        # Cleanup must not hide the real test result, so only warn.
        if response.status_code != 200:
            print(
                f"WARNING: could not delete product {product_id} "
                f"(HTTP {response.status_code})"
            )


@pytest.fixture
def post_product(admin_api, admin_url, product_cleanup):
    """Return a function that sends POST /products and registers cleanup.

    If the API creates the product (HTTP 201), its ID is remembered and
    the product is deleted automatically when the test ends.
    """

    def _post_product(payload):
        response = admin_api.post(
            f"{admin_url}/products",
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )
        if response.status_code == 201:
            product_cleanup.append(response.json()["id"])
        return response

    return _post_product