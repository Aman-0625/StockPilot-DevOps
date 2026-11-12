
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app import inventory

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_inventory():
    """Reset inventory before and after every test."""
    inventory.products.clear()
    inventory.next_id = 1
    yield
    inventory.products.clear()
    inventory.next_id = 1


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "Running"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_empty_inventory():
    response = client.get("/products")
    assert response.status_code == 200
    assert response.json() == []


def test_create_product():
    response = client.post("/products", json={
        "name": "Mouse",
        "category": "Electronics",
        "quantity": 50,
        "minimum_stock": 10,
        "price": 599
    })

    assert response.status_code == 201
    assert response.json()["id"] == 1
    assert response.json()["name"] == "Mouse"


def test_invalid_product():
    response = client.post("/products", json={
        "name": "M",
        "category": "Electronics",
        "quantity": -5,
        "minimum_stock": 10,
        "price": 599
    })

    assert response.status_code == 422


def test_product_not_found():
    response = client.get("/products/999")
    assert response.status_code == 404


def test_restock_product():
    product = client.post("/products", json={
        "name": "Keyboard",
        "category": "Electronics",
        "quantity": 10,
        "minimum_stock": 5,
        "price": 999
    })

    product_id = product.json()["id"]

    response = client.patch(
        f"/inventory/{product_id}/restock",
        json={"quantity": 20}
    )

    assert response.status_code == 200
    assert response.json()["product"]["quantity"] == 30


def test_low_stock_detection():
    client.post("/products", json={
        "name": "USB Cable",
        "category": "Accessories",
        "quantity": 2,
        "minimum_stock": 10,
        "price": 199
    })

    response = client.get("/inventory/low-stock")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_inventory_statistics():
    client.post("/products", json={
        "name": "Mouse",
        "category": "Electronics",
        "quantity": 10,
        "minimum_stock": 5,
        "price": 100
    })

    response = client.get("/stats")
    data = response.json()

    assert response.status_code == 200
    assert data["total_products"] == 1
    assert data["total_stock_units"] == 10
    assert data["total_inventory_value"] == 1000
