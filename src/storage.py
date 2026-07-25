import json
from pathlib import Path
from typing import Any

import pandas as pd


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