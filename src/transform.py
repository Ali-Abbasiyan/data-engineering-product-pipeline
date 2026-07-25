from typing import Any


def transform_product(
    product: dict[str, Any],
) -> dict[str, Any]:
    """
    Transform one valid product into a clean structure.
    """
    price = product["price"]

    discount_percentage = product.get(
        "discountPercentage",
        0,
    )

    final_price = price * (
        1 - discount_percentage / 100
    )

    return {
        "product_id": product["id"],
        "title": product["title"].strip(),
        "category": product["category"].strip().lower(),
        "brand": product.get("brand"),
        "original_price": price,
        "discount_percentage": discount_percentage,
        "final_price": round(final_price, 2),
        "rating": product.get("rating"),
        "stock": product.get("stock", 0),
    }


def transform_products(
    products: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Transform all valid products.
    """
    transformed_products: list[dict[str, Any]] = []

    for product in products:
        transformed_product = transform_product(product)
        transformed_products.append(transformed_product)

    return transformed_products