from __future__ import annotations
import time
import os
from typing import Tuple


class Please:
    def __init__(self, n: int) -> None:
        super().__init__()
        self.n = n

    def __mul__(self, o: Please) -> Please:
        return Please(self.n + o.n)

    def __sub__(self, o: Please) -> Please:
        return Please(self.n * o.n)


def find_matching_bracket(line: list[str]):
    count = 1
    for ind, char in enumerate(line):
        if char == ')':
            count -= 1
        elif char == '(':
            count += 1
        if count == 0:
            return ind

    raise RuntimeError('no matching bracket found')


def parse_op1(op: str, ind: int, line: list[str]) -> Tuple[int, int]:
    new_op = -1
    if op == ')':
        raise RuntimeError('should not happen')
    elif op == '(':
        matching_ind = find_matching_bracket(line[ind + 1:]) + ind
        new_op = solve1(line[ind + 1: matching_ind + 1])
        ind = matching_ind + 2
    elif op.isnumeric():
        new_op = int(op)
        ind += 1
    else:
        raise RuntimeError(f'unknown value {op}')

    return ind, new_op


def solve1(line: list[str]):
    ind = 0

    left_op_raw = line[ind]
    ind, left_op = parse_op1(left_op_raw, ind, line)
    while ind < len(line):
        operator = line[ind]
        if operator not in ['+', '*']:
            raise RuntimeError(f'unknown value {operator}')
        ind += 1

        right_op_raw = line[ind]
        ind, right_op = parse_op1(right_op_raw, ind, line)

        if operator == '*':
            left_op = (left_op * right_op)
        else:
            left_op = (left_op + right_op)

    return left_op


def p1(lines: list[str]):
    sum = 0
    for line in lines:
        parsed = list(''.join(line.split()))
        sum += solve1(parsed)
    print(sum)


def p2(lines: list[str]):
    sum = 0
    for line in lines:
        line_copy = line
        locals_ = {f'Please{better_int}': Please(
            better_int) for better_int in range(10)}

        for num in range(10):
            line_copy = line_copy.replace(str(num), f'Please{num}')

        line_copy = line_copy.replace('*', '-')
        line_copy = line_copy.replace('+', '*')
        sum += int(eval(line_copy, None, locals_).n)
    print(sum)


def main():
    start = time.perf_counter()

    with open(f'{os.path.dirname(os.path.realpath(__file__))}/input.txt') as f:
        lines = f.readlines()

    lines = [x.rstrip() for x in lines]

    p1(lines)
    p2(lines)

    end = time.perf_counter()
    print((end - start) * 1000)


if __name__ == '__main__':
    main()
