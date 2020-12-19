import time
import sys
from functools import reduce

# shamelessly taken from https://rosettacode.org/wiki/Chinese_remainder_theorem#Python_3.6


def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


def p1(lines: list[str]):
    earliest = int(lines[0])
    times = [int(x) for x in lines[1].split(',') if x != 'x']

    bus = 0
    best_time = sys.maxsize
    for time_ in times:
        current = earliest
        while current % time_ != 0:
            current += 1
        if current < best_time:
            best_time = current
            bus = time_

    print((best_time - earliest) * bus)


def p2(lines: list[str]):
    times = lines[1].split(',')

    n = []
    a = []
    for ind, x in enumerate(times):
        if x != 'x':
            n.append(int(x))
            a.append(int(x) - ind)

    print(chinese_remainder(n, a))


def main():
    start = time.perf_counter()

    with open('./13/input.txt') as f:
        lines = f.readlines()

    lines = [x.rstrip() for x in lines]

    p1(lines)
    p2(lines)

    end = time.perf_counter()
    print((end - start) * 1000)


if __name__ == '__main__':
    main()
