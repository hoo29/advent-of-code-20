import time
from typing import Tuple


def p1(input: list[int]):
    ind = 0
    history: dict[int, list[int]] = {}
    last = -1
    # assume input content is unique
    while ind < 2020:
        turn = ind + 1
        if ind < len(input):
            last = input[ind]
            history[last] = [turn]
        else:
            previous = history.get(last)
            if len(previous) == 1:
                last = 0
            else:
                last = previous[-1] - previous[-2]
            last_prev = history.get(last, [])
            last_prev.append(turn)
            history[last] = last_prev
        ind += 1
    print(last)


def p2(input: list[int]):
    ind = 0
    history: dict[int, list[int]] = {}
    last = -1
    # assume input content is unique
    while ind < 30000000:
        turn = ind + 1
        if ind < len(input):
            last = input[ind]
            history[last] = [turn]
        else:
            previous = history.get(last)
            if len(previous) == 1:
                last = 0
            else:
                last = previous[-1] - previous[-2]
            last_prev = history.get(last, [])
            last_prev.append(turn)
            history[last] = last_prev
        ind += 1
    print(last)


def main():
    start = time.perf_counter()

    input = [16, 1, 0, 18, 12, 14, 19]

    p1(input)
    p2(input)

    end = time.perf_counter()
    print((end - start) * 1000)


if __name__ == "__main__":
    main()
