from collections.abc import Callable
from itertools import product, permutations

# Comment out the operators you don't wish to use
OPERATORS: dict[str, Callable[[float, float], float]] = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: x / y if y != 0 else None,
    # "^": lambda x, y: None
    # if abs(y) > 1e2
    # or abs(x) > 1e3
    # or (x == 0 and y < 0)
    # or isinstance((temp := x**y), complex)
    # else temp,
    # "log": lambda x, y: None if x <= 0 or y <= 1 else math.log(x, y),
    # "%": lambda x, y: x % y if y != 0 else None,
}


def solve(target: float, numbers: list[float], tol: float = 1e-9) -> list[str]:
    """Finds all expressions that evaluate to the target with the given numbers.

    Tries all viable permutations of numbers, combinations of operators, and all
    valid RPN structures to find expressions that equal the target within tolerance.

    Args:
        target: The target value to reach.
        numbers: List of numbers to use in expressions.
        tol: Tolerance for floating point comparison. Default is 1e-9

    Returns:
        List of infix expressions that evaluate to the target.
    """
    result: list[str] = []
    attempts = 0
    n = len(numbers)
    structures = generateRPNStructures(n)
    for ops in product(OPERATORS.keys(), repeat=n - 1):
        for perm in permutations(numbers):
            for structure in structures:
                attempts += 1
                sequence = useStructures(structure, perm, ops)
                computed = computRPN(sequence)
                if computed is not None and abs(computed - target) < tol:
                    result.append(rpnToInfix(sequence))
    print(f"Attempted {attempts} expressions, found {len(result)}")
    return result


def generateRPNStructures(num: int) -> list[list[int]]:
    """Generates all valid RPN structures (ordering) for num numbers.

    Creates Catalan(num-1) distinct binary trees for the RPN where the output is
    a list of 0s and 1s to indicate operators and numbers.

    Args:
        num: number of number inputs of the RPN.

    Returns:
        List of structures represented as a list of 0s and 1s.
    """

    def generate(
        numsLeft: int, opsLeft: int, stackSize: int, cur: list[int]
    ) -> list[list[int]]:
        # Base case: placed everything
        if numsLeft == 0 and opsLeft == 0:
            return [cur[:]]
        res = []

        # Place a number if possible
        if numsLeft > 0:
            cur.append(0)
            res.extend(generate(numsLeft - 1, opsLeft, stackSize + 1, cur))
            cur.pop()

        # Place operator
        if opsLeft > 0 and stackSize >= 2:
            cur.append(1)
            res.extend(generate(numsLeft, opsLeft - 1, stackSize - 1, cur))
            cur.pop()
        return res

    return generate(num, num - 1, 0, [])


def useStructures(structure: list[int], numbers: tuple, operators: tuple) -> list:
    """Applies numbers and operators to the RPN structure.

    Args:
        structure: RPN structure. List of 0s and 1s.
        numbers: Tuple of input numbers.
        operators: Tuple of input operators.

    Returns:
        RPN with the given structure, numbers, and operators.
    """
    res = []
    numIdx = 0
    opIdx = 0
    for node in structure:
        if node == 0:
            res.append(numbers[numIdx])
            numIdx += 1
        else:
            res.append(operators[opIdx])
            opIdx += 1
    return res


def computRPN(input: list[float | str]) -> float:
    """Evaluates an RPN expression.

    Args:
        input: RPN expression as a list of numbers and operator strings.

    Returns:
        Computed result or None if evaluation fails (e.g., division by 0).
    """
    stack: list[float] = []
    for x in input:
        if type(x) is str:
            op = x
            rhs = stack.pop()
            lhs = stack.pop()
            res = OPERATORS[op](lhs, rhs)
            if res is None:
                return None
            stack.append(res)
        else:
            stack.append(x)
    return stack.pop()


def rpnToInfix(input: list[float | str]) -> str:
    """Converts an RPN expression to infix notation.

    Args:
        input: RPN expression as a list of numbers and operators.

    Returns:
        The expression in infix notation with parenthesization.
    """
    stack: list[float | str] = []
    for x in input:
        if type(x) is str:
            op = x
            rhs = stack.pop()
            lhs = stack.pop()
            stack.append(f"({lhs} {op} {rhs})")
        else:
            stack.append(x)
    return stack.pop()
