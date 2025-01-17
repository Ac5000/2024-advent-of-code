"""Code for day 7"""

import operator
import re
from dataclasses import dataclass, field
from itertools import cycle, islice, pairwise, product

OPS = ["+", "*"]


@dataclass
class Equation:
    """Represents an equation from the input"""

    test_value: int
    numbers: list[int] = field(default_factory=list)
    solvable: bool = False
    solutions: list = field(default_factory=list)
    number_pairs: list[tuple[int, int]] = field(default_factory=list)
    operator_products: list[list[str]] = field(default_factory=list)
    all_evals: list[list] = field(default_factory=list)

    def __post_init__(self):
        self.number_pairs = list(pairwise(self.numbers))
        self._generate_operators()
        self._generate_evals()

    def _generate_operators(self):
        # products = product(OPS, repeat=len(self.number_pairs))
        for pro in product(OPS, repeat=len(self.number_pairs)):
            self.operator_products.append(list(pro))

    def _generate_evals(self):
        for pro in self.operator_products:
            self.all_evals.append(list(roundrobin(self.numbers, pro)))


def get_input(filename: str) -> list[Equation]:
    """Read the file and yield rules."""
    with open(filename, "r", encoding="utf-8") as input_data:
        lines = input_data.read().splitlines()

    equations: list[Equation] = []

    for line in lines:
        split_line = re.split(": | ", line)
        equations.append(
            Equation(
                test_value=int(split_line[0]),
                numbers=[int(i) for i in split_line[1:None]],
            )
        )
    return equations


def roundrobin(*iterables):
    "Visit input iterables in a cycle until each is exhausted."
    # roundrobin('ABC', 'D', 'EF') → A D E B F C
    # Algorithm credited to George Sakkis
    iterators = map(iter, iterables)
    for num_active in range(len(iterables), 0, -1):
        iterators = cycle(islice(iterators, num_active))
        yield from map(next, iterators)


def sum_true_equations(equations: list[Equation]) -> int:
    """Sum all the equations that are solvable"""
    answer = 0
    for equation in equations:
        if equation.solvable:
            answer += equation.test_value
    print(f"Final summation = {answer}")
    return answer


def solve_equation(equation: list) -> int:
    """Run the equation for a result"""
    carry: int = 0
    operation = None
    for i, e in enumerate(equation):
        # for first value, set carry.
        if i == 0:
            carry = e
            continue
        if e == "+":
            operation = operator.add
            continue
        if e == "*":
            operation = operator.mul
            continue
        if operation is not None:
            carry = operation(carry, e)
    return carry


def evaluate_equations(equations: list[Equation]):
    """Check all the equations for solvable"""
    for equation in equations:
        for evaluation in equation.all_evals:
            # print(f"{equation.test_value=},{evaluation=}")
            if equation.test_value == solve_equation(evaluation):
                equation.solvable = True
                equation.solutions.append(evaluation)
                break


def debug_and_tests():
    """Test using the sample and examples first."""
    equations = get_input("day7example")

    # Tests for 1 pairs
    easy_test_equ_add_good = Equation(
        test_value=2, numbers=[1, 1], solvable=True
    )
    assert easy_test_equ_add_good.solvable
    easy_test_equ_mul_good = Equation(
        test_value=6, numbers=[3, 2], solvable=True
    )
    assert easy_test_equ_mul_good.solvable
    assert 8 == sum_true_equations(
        [easy_test_equ_add_good, easy_test_equ_mul_good]
    )
    assert 2 == solve_equation([2, "*", 1])
    evaluate_equations(equations)
    assert 3749 == sum_true_equations(equations)


def main():
    """Get the answer"""
    equations = get_input("day7input")
    evaluate_equations(equations)
    sum_true_equations(equations)


if __name__ == "__main__":
    debug_and_tests()
    print("THE REAL DEAL")
    main()
