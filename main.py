import json
from pathlib import Path
from typing import Any

import requests


API_URL = "https://dummyjson.com/products"
PAGE_LIMIT = 30
REQUEST_TIMEOUT = 30

RAW_OUTPUT_FILE = Path("data/raw/products.json")
VALID_OUTPUT_FILE = Path("data/processed/valid_products.json")
INVALID_OUTPUT_FILE = Path("data/rejected/invalid_products.json")


def fetch_products(
    url: str,
    limit: int = PAGE_LIMIT,
) -> list[dict[str, Any]]:
    """
    Fetch all products from a paginated API.
    """
    all_products: list[dict[str, Any]] = []
    skip = 0

    while True:
        params = {
            "limit": limit,
            "skip": skip,
        }

        response = requests.get(
            url,
            params=params,
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        data = response.json()
        products = data["products"]

        all_products.extend(products)

        print(
            f"Fetched {len(products)} products "
            f"with skip={skip}"
        )

        if len(products) < limit:
            break

        skip += limit

    return all_products


def validate_product(
    product: dict[str, Any],
) -> list[str]:
    """
    Validate one product and return its validation errors.

    An empty list means that the product is valid.
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


def save_json(
    data: list[dict[str, Any]],
    output_file: Path,
) -> None:
    """
    Save records to a JSON file.
    """
    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_file.open(
        mode="w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2,
        )


def main() -> None:
    products = fetch_products(
        url=API_URL,
        limit=PAGE_LIMIT,
    )

    save_json(
        data=products,
        output_file=RAW_OUTPUT_FILE,
    )

    valid_products, invalid_products = (
        separate_valid_and_invalid_products(products)
    )

    save_json(
        data=valid_products,
        output_file=VALID_OUTPUT_FILE,
    )

    save_json(
        data=invalid_products,
        output_file=INVALID_OUTPUT_FILE,
    )

    print("Total fetched products:", len(products))
    print("Valid products:", len(valid_products))
    print("Invalid products:", len(invalid_products))

    print("Raw data saved to:", RAW_OUTPUT_FILE)
    print("Valid data saved to:", VALID_OUTPUT_FILE)
    print("Invalid data saved to:", INVALID_OUTPUT_FILE)


if __name__ == "__main__":
    main()