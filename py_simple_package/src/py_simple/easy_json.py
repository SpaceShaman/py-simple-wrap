"""
easy_json is built to simplify working with json files
"""

import json
import os
from benedict import benedict


class EasyJsonError(Exception):
    """
    Raised when a JSON file can't be opened or parsed.

    Wraps the underlying error (missing file, bad permissions, invalid
    JSON syntax, etc.) so py_simple functions can fail with one
    consistent, easy-to-read exception instead of a random builtin one.

    Args:
        message (str): Human-readable description of what went wrong.
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def get_nested(data, path, default=None):
    """
    Safely retrieve a value from nested JSON/dict/list using dot notation.

    Args:
        data (dict | list): Parsed JSON data.
        path (str): Dot-separated path (e.g., "user.address.city" or "items.0.name").
        default (Any): Value to return if path not found. Defaults to None.

    Returns:
        Any: Value at the path, or default.
    """
    if not isinstance(data, (dict, list)):
        return default
    parts = path.split(".")
    current = data
    for part in parts:
        if isinstance(current, dict):
            if part not in current:
                return default
            current = current[part]
        elif isinstance(current, list):
            try:
                idx = int(part)
            except ValueError:
                return default
            if not (0 <= idx < len(current)):
                return default
            current = current[idx]
        else:
            return default
    return current


def open_json(filepath: str) -> dict | None:
    """
    Opens a JSON file and returns its contents as a dictionary.

    Args:
        filepath (str): Path to the JSON file to open.

    Returns:
        dict | None: The parsed JSON contents as a dictionary.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import open_json

            data = open_json("config.json")
            print(data["name"])
            ```

        === "The Traditional Way"
            ```python
            import json

            try:
                with open("config.json", encoding="utf-8") as json_file:
                    data = json.load(json_file)
                print(data["name"])
            except Exception as e:
                print(f"Couldn't read the file: {e}")
            ```
    """
    try:
        with open(filepath, encoding="utf-8") as json_file:
            return json.load(json_file)
    except Exception as e:
        raise EasyJsonError(f"\n\n\nERROR: {e}") from None


def save_json_data(filepath: str, data: dict) -> None:
    """
    Saves a dictionary to a JSON file. Raises an error if the file
    already exists, so you don't accidentally overwrite something.

    Args:
        filepath (str): Path to the JSON file to create.
        data (dict): The data to save.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import save_json_data

            save_json_data("config.json", {"name": "Sara"})
            ```

        === "The Traditional Way"
            ```python
            import json
            import os

            filepath = "config.json"
            if os.path.exists(filepath):
                print(f"File {filepath} already exists.")
            else:
                with open(filepath, "w") as json_file:
                    json.dump({"name": "Sara"}, json_file, indent=4)
            ```
    """
    if os.path.exists(filepath):
        raise EasyJsonError(f"\n\n\nERROR: File {filepath} already exists.")

    try:
        with open(filepath, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4)
    except Exception as e:
        raise EasyJsonError(f"\n\n\nERROR: {e}") from None


def pretty_json(data: dict = None, filepath: str = None) -> str | None:
    """
    Returns a pretty-printed, indented JSON string from a dictionary or
    a JSON file. Provide exactly one of `data` or `filepath` — not both.

    Args:
        data (dict): A dictionary to format as pretty-printed JSON.
        filepath (str): Path to a JSON file to load and format as
            pretty-printed JSON.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import pretty_json

            print(pretty_json(data={"name": "Sara"}))
            ```

        === "The Traditional Way"
            ```python
            import json

            print(json.dumps({"name": "Sara"}, indent=2))
            ```
    """
    if data is None and filepath is None:
        raise EasyJsonError("\n\n\nERROR: Either data or filepath "
                            "must be provided.") from None
    if data is not None and filepath is not None:
        raise EasyJsonError(f"\n\n\nERROR: Please provide data OR "
                            f"filepath.") from None
    elif data:
        return json.dumps(data, indent=2)
    else:
        try:
            d = open_json(filepath)
            return json.dumps(d, indent=2)
        except Exception as e:
            raise EasyJsonError(f"\n\n\nERROR: {e}") from None


def update_json(filepath: str, new_data: dict) -> None:
    """
    Updates a JSON file with new data, merging it into what's already
    there. Existing top-level keys in `new_data` overwrite matching keys
    in the file; anything else in the file is left untouched.

    Args:
        filepath (str): Path to the JSON file to update.
        new_data (dict): The data to merge into the existing file.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import update_json

            update_json("config.json", {"name": "Sara"})
            ```

        === "The Traditional Way"
            ```python
            import json

            with open("config.json") as json_file:
                data = json.load(json_file)

            data.update({"name": "Sara"})

            with open("config.json", "w") as json_file:
                json.dump(data, json_file, indent=4)
            ```
    """
    try:
        old_data = open_json(filepath)
        old_data.update(new_data)
        with open(filepath, "w", encoding="utf-8") as json_file:
            json.dump(old_data, json_file, indent=4)
    except Exception as e:
        raise EasyJsonError(f"\n\n\nERROR: {e}") from None


def is_json_file(filepath: str) -> bool:
    """
    Checks whether a filepath points to an existing file with a `.json`
    extension.

    Args:
        filepath (str): Path to check.

    Returns:
        bool: True if the file exists and ends in `.json`, False otherwise.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import is_json_file

            if is_json_file("config.json"):
                print("Looks good!")
            ```

        === "The Traditional Way"
            ```python
            import os

            filepath = "config.json"
            if os.path.isfile(filepath) and filepath.split(".")[-1] == "json":
                print("Looks good!")
            ```
    """
    is_file = os.path.isfile(filepath)
    if is_file:
        if filepath.split(".")[-1] == "json":
            return True
        else:
            return False
    else:
        return False


def get_json_keys(data: dict = None, filepath: str = None) -> list[str]:
    """
    Returns the top-level keys in a dictionary or JSON file.

    Provide exactly one of ``data`` or ``filepath``. This is useful when
    you want to quickly see what information a JSON object contains before
    reading a specific value.

    Args:
        data (dict): A dictionary whose keys should be returned.
        filepath (str): Path to a JSON file whose top-level keys should be
            returned.

    Returns:
        list[str]: The dictionary's top-level keys, in their original order.

    Raises:
        EasyJsonError: If neither or both of ``data``/``filepath`` are
            provided, or if the JSON data is not a dictionary.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple.easy_json import get_json_keys

            get_json_keys(data={"name": "Sara", "active": True})
            # -> ["name", "active"]
            ```

        === "The Traditional Way"
            ```python
            data = {"name": "Sara", "active": True}
            keys = list(data.keys())
            ```
    """
    if data is None and filepath is None:
        raise EasyJsonError("\n\n\nERROR: Either data or filepath "
                            "must be provided.") from None
    if data is not None and filepath is not None:
        raise EasyJsonError("\n\n\nERROR: Please provide data OR "
                            "filepath.") from None

    json_data = open_json(filepath) if filepath is not None else data
    if not isinstance(json_data, dict):
        raise EasyJsonError("\n\n\nERROR: JSON data must be a dictionary.")

    return list(json_data.keys())


def is_nested_json(data: dict = None, filepath: str = None) -> bool | None:
    """
    Checks whether a dictionary or JSON file contains any nested
    dictionaries or lists at the top level.

    Provide exactly one of `data` or `filepath` — not both.

    Args:
        data (dict): A dictionary to check for nested structures.
        filepath (str): Path to a JSON file to check for nested
            structures.

    Returns:
        bool | None: True if any top-level value is a dict or list,
            False if all top-level values are flat.

    Raises:
        EasyJsonError: If neither or both of `data`/`filepath` are
            provided, or if the file can't be opened or parsed.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import is_nested_json

            is_nested_json(data={"a": 1, "b": {"c": 2}})  # -> True
            is_nested_json(data={"a": 1, "b": 2})  # -> False
            ```

        === "The Traditional Way"
            ```python
            data = {"a": 1, "b": {"c": 2}}
            is_nested = any(
                isinstance(v, (dict, list)) for v in data.values()
            )
            ```
    """
    if data is None and filepath is None:
        raise EasyJsonError("\n\n\nERROR: Either data or filepath "
                            "must be provided.") from None
    if data is not None and filepath is not None:
        raise EasyJsonError(f"\n\n\nERROR: Please provide data OR "
                            f"filepath.") from None
    if filepath:
        to_check = open_json(filepath)
    else:
        to_check = data
    try:
        for _, value in to_check.items():
            if isinstance(value, dict) or isinstance(value, list):
                return True
            else:
                continue
    except Exception as e:
        raise EasyJsonError(f"\n\n\nERROR: {e}") from None


def flatten_json(seperator: str = "-", data: dict = None,
                 filepath: str = None) -> dict | None:
    """
    Flattens a nested dictionary or JSON file into a single-level
    dictionary, joining nested keys with `seperator`.

    Handles dicts nested inside dicts, lists nested inside dicts, and
    dicts nested inside lists, at any depth. List items are joined
    using their index (e.g. `b-0`, `b-1`). Provide exactly one of
    `data` or `filepath` — not both.

    Args:
        seperator (str): String used to join nested keys together.
            Defaults to "-".
        data (dict): A dictionary to flatten.
        filepath (str): Path to a JSON file to flatten.

    Returns:
        dict | None: A single-level dictionary with all nested values
            unwrapped into flat, uniquely-named keys.

    Raises:
        EasyJsonError: If neither or both of `data`/`filepath` are
            provided, or if the file can't be opened or parsed.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import flatten_json

            flatten_json(data={"a": 1, "b": {"c": 2}})
            # -> {"a": 1, "b-c": 2}
            ```

        === "The Traditional Way"
            ```python
            from benedict import benedict

            d = benedict({"a": 1, "b": {"c": 2}})
            flat = dict(d.flatten("-"))
            # still need to manually unwrap dicts/lists further
            ```
        """
    if data is None and filepath is None:
        raise EasyJsonError("\n\n\nERROR: Either data or filepath "
                            "must be provided.") from None
    if data is not None and filepath is not None:
        raise EasyJsonError(f"\n\n\nERROR: Please provide data OR "
                            f"filepath.") from None
    if filepath:
        nested = open_json(filepath)
    else:
        nested = data
    try:
        d = benedict(nested)
        initial_squish = d.flatten(seperator)
        flat = {}
        for key, value in initial_squish.items():
            if isinstance(value, list):
                for index, item in enumerate(value):
                    if isinstance(item, dict):
                        for key2, value2 in item.items():
                            flat[f"{key}{seperator}{index}{seperator}{key2}"] = value2
                    else:
                        flat[f"{key}{seperator}{index}"] = value[index]
            else:
                flat[key] = value
        if is_nested_json(flat):
            flat = flatten_json(seperator, flat)
            return flat
        else:
            return flat
    except Exception as e:
        raise EasyJsonError(f"\n\n\nERROR: {e}") from None
