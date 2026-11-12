
from app.models import Product, ProductCreate

# Empty inventory: products are added by users through the API
products = {}

next_id = 1


def get_all_products():
    return list(products.values())


def get_product(product_id: int):
    return products.get(product_id)


def add_product(product_data: ProductCreate):
    global next_id

    product = Product(
        id=next_id,
        **product_data.model_dump()
    )

    products[next_id] = product
    next_id += 1

    return product


def get_low_stock_products():
    return [
        product for product in products.values()
        if product.quantity <= product.minimum_stock
    ]


def restock_product(product_id: int, quantity: int):
    product = products.get(product_id)

    if product is None:
        return None

    updated_product = product.model_copy(
        update={"quantity": product.quantity + quantity}
    )

    products[product_id] = updated_product

    return updated_product


def get_inventory_stats():
    all_products = list(products.values())

    return {
        "total_products": len(all_products),
        "total_stock_units": sum(p.quantity for p in all_products),
        "total_inventory_value": sum(
            p.quantity * p.price for p in all_products
        ),
        "low_stock_count": len(get_low_stock_products())
    }
