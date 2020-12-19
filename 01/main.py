from typing import List
import time

max_value = 2020


def find_value1(expenses: List[int]):
    for ind1, val1 in enumerate(expenses):
        for val2 in expenses[ind1 + 1:]:
            if val1 + val2 > max_value:
                break
            if val1 + val2 == max_value:
                return val1 * val2


def p1(expenses: List[int]):
    value = find_value1(expenses)
    print(value)


def find_value2(expenses: List[int]):
    for ind1, val1 in enumerate(expenses):
        for ind2, val2 in enumerate(expenses[ind1 + 1:]):
            if val1 + val2 > max_value:
                break
            for val3 in expenses[ind2 + 1:]:
                if val1 + val2 + val3 == max_value:
                    return val1 * val2 * val3
                if val1 + val2 + val3 > max_value:
                    break


def p2(expenses: List[int]):
    value = find_value2(expenses)
    print(value)


if __name__ == '__main__':
    start = time.perf_counter()

    with open('./1/input.txt') as f:
        expenses = f.readlines()

    # take off \n
    expenses = [int(x.rstrip()) for x in expenses]
    # remove values that will never work
    expenses = [x for x in expenses if x + min(expenses) <= max_value]
    # sort for early break out
    expenses.sort()

    p1(expenses)
    p2(expenses)

    end = time.perf_counter()
    print((end - start) * 1000)
