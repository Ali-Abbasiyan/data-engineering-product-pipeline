from typing import Any


def validate_product(
    product: dict[str, Any],
) -> list[str]:
    """
    Validate one product and return validation errors.

    An empty list means the product is valid.
    """
    errors: list[str] = []

    product_id = product.get("id")
    title = product.get("title")
    price = product.get("price")
    category = product.get("category")

    if not isinstance(product_id, int) or product_id <= 0:
        errors.append("id must be a positive integer")

    if not isinstance(title, str) or not title.strip():
        errors.append("title must be a non-empty string")

    if (
        not isinstance(price, (int, float))
        or isinstance(price, bool)
        or price < 0
    ):
        errors.append("price must be a non-negative number")

    if not isinstance(category, str) or not category.strip():
        errors.append("category must be a non-empty string")

    return errors


def separate_valid_and_invalid_products(
    products: list[dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    """
    Separate valid products from invalid products.
    """
    valid_products: list[dict[str, Any]] = []
    invalid_products: list[dict[str, Any]] = []

    for product in products:
        errors = validate_product(product)

        if errors:
            invalid_products.append(
                {
                    "product": product,
                    "validation_errors": errors,
                }
            )
        else:
            valid_products.append(product)

    return valid_products, invalid_products