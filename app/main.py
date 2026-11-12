
from fastapi import FastAPI, HTTPException, status

from app.models import ProductCreate, RestockRequest
from app import inventory

app = FastAPI(
    title="StockPilot API",
    description="Inventory Management System",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to StockPilot",
        "status": "Running"
    }


@app.get("/products")
def get_products():
    return inventory.get_all_products()


@app.get("/products/{product_id}")
def get_product(product_id: int):
    product = inventory.get_product(product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):
    return inventory.add_product(product)


@app.get("/inventory/low-stock")
def low_stock():
    return inventory.get_low_stock_products()


@app.patch("/inventory/{product_id}/restock")
def restock(product_id: int, request: RestockRequest):
    product = inventory.restock_product(
        product_id,
        request.quantity
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return {
        "message": "Stock updated successfully",
        "product": product
    }


@app.get("/stats")
def statistics():
    return inventory.get_inventory_stats()


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "application": "StockPilot"
    }
