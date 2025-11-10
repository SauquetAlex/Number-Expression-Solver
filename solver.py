from functools import partial
from itertools import permutations, product
from multiprocessing import Pool, cpu_count

from operators import OPERATORS


def solve(
    target: float,
    numbers: list[float],
    tol: float = 1e-9,
    max_workers: int | None = None,
) -> list[str]:
    """Finds all expressions that evaluate to the target with the given numbers.

    Tries all viable permutations of numbers, combinations of operators, and all
    valid RPN structures to find expressions that equal the target within
    tolerance.

    Args:
        target: The target value to reach.
        numbers: List of numbers to use in expressions.
        tol: Tolerance for floating point comparison. Default is 1e-9
        max_workers: Number of workers for multiprocessing. Default will use as
            many as there are cpus.

    Returns:
        List of infix expressions that evaluate to the target.
    """
    result: list[str] = []
    attempts = 0
    n = len(numbers)
    structures = generateRPNStructures(n)
    opsCombinations = list(product(OPERATORS.keys(), repeat=n - 1))
    worker = partial(
        processOpsCombinations,
        target=target,
        numbers=numbers,
        structures=structures,
        tol=tol,
    )

    if max_workers is None:
        max_workers = cpu_count()
    with Pool(max_workers) as pool:
        results = pool.map(worker, opsCombinations)
    result = [expr for sublist in results for expr in sublist]

    attempts = len(opsCombinations) * len(list(permutations(numbers))) * len(structures)
    print(f"Attempted {attempts} expressions, found {len(result)}")
    return result


def processOpsCombinations(
    operators: tuple[str, ...],
    target: float,
    numbers: list[float],
    structures: list[list[int]],
    tol: float,
) -> list[str]:
    """Processes all expressions for a specific combinations of operators.

    Process called by each worker for each combination of operators. Tests every
    permutation and structure possilbe and reports the solutions found.

    Args:
        ops: Given combination of operators.
        target: The target value to reach.
        numbers: List of numbers to use in expressions.
        structures: Precomputed structures of RPN to use.
        tol: Tolerance for floating point comparison. Default is 1e-9

    Returns:
        All operations that result in reaching the target.
    """
    res = []
    for perm in permutations(numbers):
        for structure in structures:
            sequence = useStructures(structure, perm, operators)
            computed = computeRPN(sequence)
            if computed is not None and abs(computed - target) < tol:
                res.append(rpnToInfix(sequence))
    return res


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


def useStructures(
    structure: list[int], numbers: tuple[float, ...], operators: tuple[str, ...]
) -> list:
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


def computeRPN(input: list[float | str]) -> float | None:
    """Evaluates an RPN expression.

    Args:
        input: RPN expression as a list of numbers and operator strings.

    Returns:
        Computed result or None if evaluation fails (e.g., division by 0).
    """
    stack: list[float] = []
    for x in input:
        if isinstance(x, str):
            op = x
            rhs = stack.pop()
            lhs = stack.pop()
            res = OPERATORS[op].func(lhs, rhs)
            if res is None:
                return None
            stack.append(res)
        else:
            stack.append(x)
    return stack.pop()


def rpnToInfix(input: list[float | str]) -> str | None:
    """Converts an RPN expression to infix notation.

    Args:
        input: RPN expression as a list of numbers and operators.

    Returns:
        The expression in infix notation with parenthesization.
    """
    if not input:
        return None

    stack: list[tuple[str, str | None, float]] = []

    for x in input:
        if type(x) is str:
            op = x
            rhsExpr, rhsOp, rhsPrec = stack.pop()
            lhsExpr, lhsOp, lhsPrec = stack.pop()
            currPrec = OPERATORS[op].precedence
            currAssoc = OPERATORS[op].associative

            if lhsOp is not None and lhsPrec < currPrec:
                lhsExpr = f"({lhsExpr})"
            if rhsOp is not None and (
                rhsPrec < currPrec or (rhsPrec == currPrec and not currAssoc)
            ):
                rhsExpr = f"({rhsExpr})"

            result = f"{lhsExpr} {op} {rhsExpr}"
            stack.append((result, op, currPrec))
        else:
            stack.append((str(x), None, float("inf")))
    return stack[0][0]
