import time
from typing import Tuple


def move(x: int, y: int, action: str, value: int):
    if action == 'N':
        y += value
    elif action == 'S':
        y -= value
    elif action == 'E':
        x += value
    elif action == 'W':
        x -= value

    return x, y


def p1(lines: list[Tuple[str, int]]):

    dirs = ['N', 'E', 'S', 'W']
    dir_ = 'E'
    x = 0
    y = 0
    for line in lines:
        action = line[0]
        value = line[1]
        if action in dirs:
            x, y = move(x, y, action, value)
        elif action == 'L':
            diff = int(value / 90)
            dir_ = dirs[(dirs.index(dir_) - diff) % 4]
        elif action == 'R':
            diff = int(value / 90)
            dir_ = dirs[(dirs.index(dir_) + diff) % 4]
        elif action == 'F':
            x, y = move(x, y, dir_, value)
        else:
            raise RuntimeError(f"unknown action f{action}")

    print(abs(x) + abs(y))


def p2(lines: list[Tuple[str, int]]):
    dirs = ['N', 'E', 'S', 'W']
    x = 0
    y = 0
    wx = 10
    wy = 1
    for line in lines:
        action = line[0]
        value = line[1]
        if action in dirs:
            wx, wy = move(wx, wy, action, value)
        elif action == 'L' or action == 'R':
            diff = int(value / 90)
            if diff == 3:
                action = 'R' if action == 'L' else 'L'
                diff = 1
            if diff == 1:
                temp_wy = wy
                wy = wx if action == 'L' else -wx
                wx = -temp_wy if action == 'L' else temp_wy
            elif diff == 2:
                wx = -wx
                wy = -wy
        elif action == 'F':
            x += wx * value
            y += wy * value
        else:
            raise RuntimeError(f"unknown action f{action}")

    print(abs(x) + abs(y))


def main():
    start = time.perf_counter()

    with open('./12/input.txt') as f:
        lines = f.readlines()

    lines = [(x.rstrip()[0], int(x.rstrip()[1:])) for x in lines]

    p1(lines)
    p2(lines)

    end = time.perf_counter()
    print((end - start) * 1000)


if __name__ == "__main__":
    main()
