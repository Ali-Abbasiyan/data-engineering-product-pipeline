import json
from pathlib import Path
from typing import Any

import pandas as pd

from src.extract import fetch_products
from src.validate import separate_valid_and_invalid_products


API_URL = "https://dummyjson.com/products"
PAGE_LIMIT = 30

RAW_OUTPUT_FILE = Path("data/raw/products.json")
PROCESSED_OUTPUT_FILE = Path("data/processed/products.json")
PARQUET_OUTPUT_FILE = Path("data/processed/products.parquet")
INVALID_OUTPUT_FILE = Path("data/rejected/invalid_products.json")


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


def save_parquet(
    data: list[dict[str, Any]],
    output_file: Path,
) -> None:
    """
    Save records to a Parquet file.
    """
    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    dataframe = pd.DataFrame(data)

    dataframe.to_parquet(
        output_file,
        index=False,
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

    transformed_products = transform_products(
        valid_products
    )

    save_json(
        data=transformed_products,
        output_file=PROCESSED_OUTPUT_FILE,
    )

    save_parquet(
        data=transformed_products,
        output_file=PARQUET_OUTPUT_FILE,
    )

    save_json(
        data=invalid_products,
        output_file=INVALID_OUTPUT_FILE,
    )

    print("Total fetched products:", len(products))
    print("Valid products:", len(valid_products))
    print("Invalid products:", len(invalid_products))
    print(
        "Transformed products:",
        len(transformed_products),
    )

    print("Raw data saved to:", RAW_OUTPUT_FILE)
    print(
        "Processed JSON saved to:",
        PROCESSED_OUTPUT_FILE,
    )
    print(
        "Processed Parquet saved to:",
        PARQUET_OUTPUT_FILE,
    )
    print(
        "Invalid data saved to:",
        INVALID_OUTPUT_FILE,
    )


if __name__ == "__main__":
    main()