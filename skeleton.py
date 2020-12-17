import time
import os


def p1(lines: list[str]):
    print('p1')


def p2(lines: list[str]):
    print('p2')


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
