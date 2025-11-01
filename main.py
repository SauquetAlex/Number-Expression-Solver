#!/usr/bin/env python3
from solver import solve

if __name__ == "__main__":
    # Example: solve the 24 game
    print("Solving for 24 using [2, 4, 8, 12]:")
    for result in solve(24, [2, 4, 8, 12]):
        print(result)

    print("\nSolving for 67 using [1, 2, 3, 4, 5]:")
    for result in solve(67, [1, 2, 3, 4, 5]):
        print(result)
