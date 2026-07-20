import json
from pathlib import Path

import requests


url = "https://dummyjson.com/products"

limit = 30
skip = 0

all_products = []

while True:
    params = {
        "limit": limit,
        "skip": skip,
    }

    response = requests.get(
        url,
        params=params,
        timeout=30,
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


raw_directory = Path("data/raw")
raw_directory.mkdir(parents=True, exist_ok=True)

output_file = raw_directory / "products.json"

with output_file.open(
    mode="w",
    encoding="utf-8",
) as file:
    json.dump(
        all_products,
        file,
        ensure_ascii=False,
        indent=2,
    )


print("Total fetched products:", len(all_products))
print("Raw data saved to:", output_file)