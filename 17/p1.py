import time
import os
import copy


def init_grid(cycles: int, lines: list[str]):
    grid: list[list[list[str]]] = []
    grow = cycles + 1
    x_range = len(lines[0]) + (grow * 2)
    y_range = len(lines) + (grow * 2)
    z_range = (grow * 2) + 1

    for y in range(y_range):
        grid.append([])
        for x in range(x_range):
            grid[y].append([])
            for z in range(z_range):
                if z == z_range // 2 and grow <= x < (grow + len(lines[0])) and grow <= y < (grow + len(lines)):
                    grid[y][x].append(lines[y - grow][x - grow])
                else:
                    grid[y][x].append('.')
    return grid


def get_neighbours(grid: list[list[list[str]]], x: int, y: int, z: int):
    x_range = [x - 1, x, x + 1]
    y_range = [y - 1, y, y + 1]
    z_range = [z - 1, z, z + 1]

    if x_range[0] < 0 or y_range[0] < 0 or z_range[0] < 0:
        raise RuntimeError('init lower violation')

    if x_range[2] >= len(grid) or y_range[2] >= len(grid[0]) or z_range[2] >= len(grid[0][0]):
        raise RuntimeError('init upper violation')

    neighbours: list[list[list[str]]] = []
    for grid_x_ind, grid_x in enumerate(x_range):
        neighbours.append([])
        for grid_y_ind, grid_y in enumerate(y_range):
            neighbours[grid_x_ind].append([])
            for _, grid_z in enumerate(z_range):
                if grid_x == x and grid_y == y and grid_z == z:
                    neighbours[grid_x_ind][grid_y_ind].append('%')
                else:
                    neighbours[grid_x_ind][grid_y_ind].append(
                        grid[grid_x][grid_y][grid_z])

    return neighbours


def count_grid(grid: list[list[list[str]]], char: str):
    count = 0
    for x_ind in range(len(grid)):
        for y_ind in range(len(grid[x_ind])):
            for z_ind in range(len(grid[x_ind][y_ind])):
                if grid[x_ind][y_ind][z_ind] == char:
                    count += 1
    return count


def p1(lines: list[str]):
    cycles = 6
    grid = init_grid(cycles, lines)
    new_grid = []

    for cycle in range(cycles):
        new_grid = copy.deepcopy(grid)
        x_range = range(cycles - cycle, len(lines[0]) + cycles + cycle + 2)
        y_range = range(cycles - cycle, len(lines) + cycles + cycle + 2)
        z_range = range(cycles - cycle, cycles + cycle + 3)
        for x in x_range:
            for y in y_range:
                for z in z_range:
                    neighbour_grid = get_neighbours(grid, x, y, z)
                    active_count = count_grid(neighbour_grid, '#')
                    if grid[x][y][z] == '#' and not (2 <= active_count <= 3):
                        new_grid[x][y][z] = '.'
                    elif grid[x][y][z] == '.' and active_count == 3:
                        new_grid[x][y][z] = '#'
        grid = new_grid

    final_count = count_grid(grid, '#')
    print(final_count)


def main():
    start = time.perf_counter()

    with open(f'{os.path.dirname(os.path.realpath(__file__))}/input.txt') as f:
        lines = f.readlines()

    lines = [x.rstrip() for x in lines]

    p1(lines)

    end = time.perf_counter()
    print((end - start) * 1000)


if __name__ == '__main__':
    main()
