from typing import Any

import requests


PAGE_LIMIT = 30
REQUEST_TIMEOUT = 30


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