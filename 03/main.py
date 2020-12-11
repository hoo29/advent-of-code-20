from typing import List
import time
import math


def p1(grid: List[str]):
    count = 0

    right = 3
    down = 1

    x = right
    y = down

    while y < len(grid):

        line = grid[y]
        char_at_loc = line[x % len(line)]
        if char_at_loc == '#':
            count += 1
        x += right
        y += down

    print(count)


def count_trees(grid: List[str], right: int, down: int):
    count = 0

    x = right
    y = down

    while y < len(grid):

        line = grid[y]
        char_at_loc = line[x % len(line)]
        if char_at_loc == '#':
            count += 1
        x += right
        y += down

    return count


def p2(grid: List[str]):
    slopes = [
        {"right": 1, "down": 1},
        {"right": 3, "down": 1},
        {"right": 5, "down": 1},
        {"right": 7, "down": 1},
        {"right": 1, "down": 2}
    ]

    totals = [count_trees(grid, slope["right"], slope["down"])
              for slope in slopes]
    total = math.prod(totals)
    print(total)


def main():
    start = time.perf_counter()

    with open('./3/input.txt') as f:
        grid = f.readlines()

    grid = [x.rstrip() for x in grid]

    p1(grid)
    p2(grid)

    end = time.perf_counter()
    print((end - start) * 1000)


if __name__ == "__main__":
    main()
