from collections.abc import Callable
from dataclasses import dataclass
import math


@dataclass
class Operator:
    """Defines an operator with its function, precedence, and associativity.

    Attributes:
        func: Binary function that takes two floats and returns float or None
        precedence: Integer precedence level (higher indicates earlier compute)
            Could be negative to indicate bitwise operations, but precedence
            level should follow conventions.
        associative: Whether the operator is associative.
    """

    func: Callable[[float, float], float | None]
    precedence: int
    associative: bool

# Comment in/out operators you wish to use or add your own.
OPERATORS: dict[str, Operator] = {
    "+": Operator(
        func=lambda x, y: x + y,
        precedence=1,
        associative=True,
    ),
    "-": Operator(
        func=lambda x, y: x - y,
        precedence=1,
        associative=False,
    ),
    "*": Operator(
        func=lambda x, y: x * y,
        precedence=2,
        associative=True,
    ),
    "/": Operator(
        func=lambda x, y: x / y if y != 0 else None,
        precedence=2,
        associative=False,
    ),
    # "**": Operator(
    #     func=lambda x, y: None
    #     if abs(y) > 1e2
    #     or abs(x) > 1e3
    #     or (x == 0 and y < 0)
    #     or isinstance((temp := x**y), complex)
    #     else temp,
    #     precedence=5,
    #     associative=False,
    # ),
    # "logbase": Operator(
    #     func=lambda x, y: None if x <= 0 or y <= 1 else math.log(x, y),
    #     precedence=4,
    #     associative=False,
    # ),
    # "%": Operator(
    #     func=lambda x, y: x % y if y != 0 else None,
    #     precedence=2,
    #     associative=False,
    # ),
}
