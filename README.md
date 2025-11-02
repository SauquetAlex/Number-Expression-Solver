# Number Expression Solver

[![License: NON-AI-MIT](https://img.shields.io/badge/License-NON--AI--MIT-blue.svg)](https://github.com/non-ai-licenses/non-ai-licenses)

A Python solver that finds all possible mathematical expressions given a set of numbers to reach a target value.

## Description

Given a target number and a list of numbers, this solver exhaustively searches through all possible combinations of operations (+, -, *, /) and orderings to find valid expressions. This solver can solve puzzles like the "24 game" or "numbers round" from the game show Countdown.

You can run the solver directly by cloning or downloading the script.

## Features

- Exhaustive search through all valid expression trees.
- Support for basic operators: addition, subtraction, multiplication, division.
- Extensible operator system (commented code shows how to add exponentiation, logarithms, and modulo) with precedence and associativity.
- Uses Reverse Polish Notation (RPN) internally for efficient computation and generating expression trees.
- Outputs results in readable infix notation with minimal parenthesizing.
- Configurable tolerance for target matching.
- Configurable number of workers for multiprocessing.

## Usage

### Basic example
```python
from solver import solve

# Finds all ways of making 24 using the numbers 2, 4, 8, 12
results = solve(24, [2, 4, 8, 12])
for expr in results:
    print(expr)
```
You can modify the examples in `main.py` and run them with:
```bash
python3 main.py
```
### Customizing Operators and Tolerance

Edit the `OPERATORS` dictionary in `operators.py` to enable/disable operators:
```python
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
```
Note that more complicated operators require additional checks to keep the solver efficient and avoid errors.

You can modify the precision of the solver via the `tol` parameter. Tolerance is needed when working with floating-point numbers.

## How it works

The solver uses four key techniques:

1. **RPN Structure Generation**: Generates all valid RPN structures (binary trees) with a recursive algorithm.
2. **Exhaustive Search**: Tries all combinations of:
  - Number permutations
  - Operator combinations
  - Expression structures
3. **Stack-Based Evaluation**: Evaluates the RPN expressions and converts them to readable infix notation.
4. **Multiprocessing**: The solver uses a different worker for each combinations of operators.

The number of attempts grows factorially with the number of inputs, so the solver is intended for 4-6 input numbers.

## Credits

- **Alexandre Sauquet**: Project structure, RPN structure generation, generalization of the algorithm, and documentation.
- **Kian Kasad**: Original solver algorithm and RPN implementations.

## License

This project is licensed under the NON-AI-MIT License - see the [LICENSE](LICENSE) file for details.

This license prohibits the use of this software for training or improving machine learning algorithms.
