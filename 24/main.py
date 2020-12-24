import time
import os
import re
import copy
from typing import Tuple, Union
from collections import deque


class Floor:
    def __init__(self) -> None:
        super().__init__()
        self.pos_y: list[Tuple[list[bool], list[bool]]] = []
        self.neg_y: list[Tuple[list[bool], list[bool]]] = []
        self.b_count = 0
        self.flip_count = 0
        self.double_flip_count = 0

    def flip_tile(self, x: int, y: int):
        self.flip_count += 1

        if y >= 0:
            y_axis = self.pos_y
        else:
            y_axis = self.neg_y
        y = abs(y)

        while len(y_axis) <= y:
            y_axis.append(([], []))

        if x >= 0:
            x_axis = y_axis[y][1]
        else:
            x_axis = y_axis[y][0]
        x = abs(x)

        while len(x_axis) <= x:
            x_axis.append(False)

        x_axis[x] = not x_axis[x]

        if x_axis[x]:
            self.b_count += 1
        else:
            self.b_count -= 1
            self.double_flip_count += 1

    def check_grid(self):
        count = 0
        for y in [*self.neg_y, *self.pos_y]:
            count += [*y[0], *y[1]].count(True)
        return count

    def combine_grids(self):
        min_x = 0
        max_x = 0
        min_y = len(self.neg_y)
        max_y = len(self.pos_y)

        for i in range(len(self.pos_y)):
            len_pos_x = len(self.pos_y[i][1])
            len_neg_x = len(self.pos_y[i][0])
            max_x = max(len_pos_x, max_x)
            min_x = max(len_neg_x, min_x)

        for i in range(len(self.neg_y)):
            len_pos_x = len(self.neg_y[i][1])
            len_neg_x = len(self.neg_y[i][0])
            max_x = max(len_pos_x, max_x)
            min_x = max(len_neg_x, min_x)
        grid: deque[deque[bool]] = deque()

        for y in range((-min_y + 1), max_y):
            line: deque[bool] = deque()
            for x in range((-min_x + 1), max_x):
                if y >= 0:
                    y_axis = self.pos_y
                else:
                    y_axis = self.neg_y
                new_y = abs(y)
                try:
                    if x >= 0:
                        x_axis = y_axis[new_y][1]
                    else:
                        x_axis = y_axis[new_y][0]
                    new_x = abs(x)
                    value = x_axis[new_x]
                except IndexError:
                    value = False
                line.append(value)
            grid.append(line)
        return grid


def p1(lines: list[str]):
    floor = Floor()
    pattern = re.compile(r'e|se|sw|w|nw|ne')

    for line in lines:
        x = 0
        y = 0

        matches = re.findall(pattern, line)
        for match in matches:

            if match == 'e':
                x += 2
            elif match == 'w':
                x -= 2
            elif match == 'se':
                x += 1
                y -= 1
            elif match == 'sw':
                x -= 1
                y -= 1
            elif match == 'nw':
                x -= 1
                y += 1
            elif match == 'ne':
                x += 1
                y += 1
            else:
                raise RuntimeError(f'unknown dir {match}')
        floor.flip_tile(x, y)

    print(floor.b_count)
    return floor


def count_black_tiles(grid: Union[list[list[bool]], deque[deque[bool]]]):
    count = 0
    for y in range(len(grid)):
        count += grid[y].count(True)
    return count


def count_black_neighbours(grid: deque[deque[bool]], x: int, y: int):
    neighbours = [
        # e
        (2, 0),
        # se
        (1, -1),
        # sw
        (-1, -1),
        # w
        (-2, 0),
        # nw
        (-1, 1),
        # ne
        (1, 1)
    ]
    count = 0
    for neighbour in neighbours:
        try:
            if grid[y + neighbour[1]][x + neighbour[0]]:
                count += 1
        except IndexError:
            pass
    return count


def print_grid(grid: deque[deque[bool]]):
    for y in grid:
        line = ''
        for x in y:
            line += f'{x:<3}'
        print(line)


def p2(floor: Floor):
    grid = floor.combine_grids()
    print(floor.check_grid())
    print(count_black_tiles(grid))
    print_grid(grid)
    x_len = len(grid[0])
    new_line = deque()
    for _ in range(x_len):
        new_line.append(False)

    for day in range(100):
        for _ in range(2):
            new_line.append(False)

        for y in grid:
            y.appendleft(False)
            y.append(False)

        grid.appendleft(new_line.copy())
        grid.append(new_line.copy())

        day_grid = copy.deepcopy(grid)

        for y_ind, y in enumerate(grid):
            x_ind = 0
            while x_ind < len(y):
                x = y[x_ind]
                count = count_black_neighbours(grid, x_ind, y_ind)
                if x and (count == 0 or count > 2):
                    day_grid[y_ind][x_ind] = False
                elif not x and count == 2:
                    day_grid[y_ind][x_ind] = True
                x_ind += 1

        print(f'day {day + 1}: {count_black_tiles(day_grid)}')

        grid = day_grid


def main():
    start = time.perf_counter()

    with open(f'{os.path.dirname(os.path.realpath(__file__))}/input.txt') as f:
        lines = f.readlines()

    lines = [x.rstrip() for x in lines]

    floor = p1(lines)
    p2(floor)

    end = time.perf_counter()
    print((end - start) * 1000)


if __name__ == '__main__':
    main()
