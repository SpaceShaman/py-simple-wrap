# Easy Logging

Recording when an operation starts, finishes, or fails often means repeating the same logging calls. The `easy_logging` module wraps Python's standard `logging` module with helpers for code blocks, functions, and methods.

## A small real-world example

Imagine you're preparing an order summary and want to see which customer's total is being calculated.

```python
import logging
from py_simple import log_function, log_step

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


@log_function("Calculate total for {customer}")
def calculate_total(customer: str, prices: list[float], discount: float = 0) -> float:
    return sum(prices) - discount


with log_step("Prepare order summary"):
    total = calculate_total("Ada", [20, 30], discount=5)
```

Example output:

```text
INFO: Starting: Prepare order summary
INFO: Starting: Calculate total for Ada
INFO: Finished: Calculate total for Ada
INFO: Finished: Prepare order summary
```

## What happened?

`logging.basicConfig()` enables INFO messages and sets their format. Configure logging once when your application starts; these helpers use the root logger and its existing configuration.

`log_step()` logs entry into the `with` block and its successful completion.

`log_function()` logs the function call and replaces `{customer}` with `"Ada"`. Templates can use positional arguments, keyword arguments, and default values for omitted arguments. The function still returns its normal result, so `total` is `45`. The decorator also works on synchronous methods; `self` and `cls` are excluded from template fields.

If a block or decorated function raises an exception, the helper logs an ERROR message with the traceback and re-raises the original exception. It does not log a successful completion for that operation.

## Why use these helpers?

These helpers handle the repeated start, success, and failure logging around an operation, keeping the code focused on its task. Use `log_step()` for a selected block and `log_function()` when every call to a synchronous function or method should be logged.

See the [Easy Logging reference](../reference/easy_logging.md) for argument details and examples alongside their standard-library equivalents.

## Further reading

For the reasoning behind these helpers and a walkthrough of using context managers and decorators for logging, read [How to Add Logging Without Cluttering Your Code](https://spaceshaman.github.io/posts/how-to-add-logging-without-cluttering-your-code/) by SpaceShaman.
