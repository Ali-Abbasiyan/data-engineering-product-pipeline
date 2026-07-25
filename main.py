import json
from pathlib import Path
from typing import Any

import requests


API_URL = "https://dummyjson.com/products"
PAGE_LIMIT = 30
REQUEST_TIMEOUT = 30

RAW_DIRECTORY = Path("data/raw")
RAW_OUTPUT_FILE = RAW_DIRECTORY / "products.json"


def fetch_products(
    url: str,
    limit: int = PAGE_LIMIT,
) -> list[dict[str, Any]]:
    """
    Fetch all products from a paginated API.

    Args:
        url: API endpoint.
        limit: Number of products requested per page.

    Returns:
        A list containing all fetched products.
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


def save_json(
    data: list[dict[str, Any]],
    output_file: Path,
) -> None:
    """
    Save data as a JSON file.

    Args:
        data: Records that should be saved.
        output_file: Destination file path.
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

    print("Total fetched products:", len(products))
    print("Raw data saved to:", RAW_OUTPUT_FILE)


if __name__ == "__main__":
    main()