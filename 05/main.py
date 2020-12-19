import time
import math


def bsp(code: str, max_value: int):
    low = 0
    high = max_value

    lower_chars = ['F', 'L']
    upper_chars = ['B', 'R']

    for char in code:
        if char in lower_chars:
            high -= math.ceil((high - low) / 2)
        elif char in upper_chars:
            low += math.ceil((high - low) / 2)
        else:
            raise RuntimeError(f'unknown char {char}')

    if low != high:
        raise RuntimeError(f'error {low} != {high}')

    return low


def p1(passes: list[str]):
    rows = 127
    columns = 7

    row_char_count = 7
    column_char_count = 3

    seat_ids = []

    for item in passes:
        row_code = item[:row_char_count]
        row = bsp(row_code, rows)

        column_code = item[-column_char_count:]
        column = bsp(column_code, columns)
        seat_ids.append((row * 8) + column)

    print(max(seat_ids))


def p2(passes: list[str]):
    rows = 127
    columns = 7

    row_char_count = 7
    column_char_count = 3

    seat_ids = []

    for item in passes:
        row_code = item[:row_char_count]
        row = bsp(row_code, rows)

        column_code = item[-column_char_count:]
        column = bsp(column_code, columns)

        seat_ids.append((row * 8) + column)

    seat_ids.sort()
    for ind, seat_id in enumerate(seat_ids):
        if seat_ids[ind + 1] != seat_id + 1:
            print(seat_id + 1)
            return


def main():
    start = time.perf_counter()

    with open('./5/input.txt') as f:
        passes = f.readlines()

    passes = [x.rstrip() for x in passes]

    p1(passes)
    p2(passes)

    end = time.perf_counter()
    print((end - start) * 1000)


if __name__ == '__main__':
    main()
