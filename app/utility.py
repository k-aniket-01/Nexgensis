import json
import math
from pathlib import Path
from typing import Any

from app.schemas import Point


def load_json(file_path: Path) -> dict[str, Any]:

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    if not file_path.is_file():
        raise ValueError(
            f"Path is not a file: {file_path}"
        )

    try:
        with file_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON in {file_path}: "
            f"line {exc.lineno}, "
            f"column {exc.colno}"
        ) from exc

    if not isinstance(data, dict):
        raise ValueError(
            "Root JSON value must be an object."
        )

    return data


def save_json(data: dict[str, Any], file_path: Path):

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with file_path.open("w", encoding="utf-8"
    ) as file:
        json.dump(data, file, indent=4)
        file.write("\n")


def calculate_distance(start: Point, end: Point):

    data = math.hypot(
            end[0] - start[0],
            end[1] - start[1],
        )
    return data