import time
import cProfile

# not the best performance


def gen_adj_grid(lines: list[str], y: str, y_ind: int, x_ind: int):
    adj = []
    for line in range(max(y_ind - 1, 0), min(len(lines), y_ind + 2)):
        adj.append(lines[line][max(x_ind-1, 0): min(len(y), x_ind+2)])
    return adj


def count_char_in_grid(grid: list[str], char: str):
    count = 0
    for line in grid:
        count += line.count(char)
    return count


def char_filled_seats(grid: list[str], start_x: int, start_y: int, direction: str):

    y = start_y
    x = start_x

    while True:
        if 'n' in direction:
            y -= 1

        if 'e' in direction:
            x += 1

        if 's' in direction:
            y += 1

        if 'w' in direction:
            x -= 1

        if not (0 <= y < len(grid) and 0 <= x < len(grid[0])):
            return 0

        if grid[y][x] == 'L':
            return 0

        if grid[y][x] == '#':
            return 1


def p1(plan: list[str]):
    new_plan = []
    new_line = []
    for y_ind, y in enumerate(plan):
        for x_ind, x in enumerate(y):
            adj_grid = gen_adj_grid(plan, y, y_ind, x_ind)
            occupied_count = count_char_in_grid(adj_grid, '#')

            if x == '#':
                occupied_count -= 1

            if x == '.':
                char = '.'
            elif x == 'L':
                char = '#' if occupied_count == 0 else 'L'
            elif x == '#':
                char = 'L' if occupied_count >= 4 else '#'
            else:
                raise RuntimeError(f'well something has really gone wrong {x}')

            new_line.append(char)

        new_plan.append(new_line)
        new_line = []

    # print()
    # for line in new_plan:
    #     print(line)
    # print()
    if new_plan == plan:
        return new_plan
    else:
        return p1(new_plan)


def p2(plan: list[str]):
    new_plan = []
    new_line = []
    dirs = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
    for y_ind, y in enumerate(plan):
        for x_ind, x in enumerate(y):
            occupied_count = 0
            for dir_ in dirs:
                occupied_count += char_filled_seats(plan,  x_ind, y_ind, dir_)

            if x == '.':
                char = '.'
            elif x == 'L':
                char = '#' if occupied_count == 0 else 'L'
            elif x == '#':
                char = 'L' if occupied_count >= 5 else '#'
            else:
                raise RuntimeError(f'well something has really gone wrong {x}')

            new_line.append(char)

        new_plan.append(new_line)
        new_line = []

    # print()
    # for line in new_plan:
    #     print(line)
    # print()
    if new_plan == plan:
        return new_plan
    else:
        return p2(new_plan)


def main():
    start = time.perf_counter()

    with open('./11/input.txt') as f:
        lines = f.readlines()

    lines = [list(x.rstrip()) for x in lines]

    final = p1(lines)
    count = count_char_in_grid(final, '#')
    print(count)

    final2 = p2(lines)
    count2 = count_char_in_grid(final2, '#')
    print(count2)

    end = time.perf_counter()
    print((end - start) * 1000)


if __name__ == "__main__":
    cProfile.run("main()")
