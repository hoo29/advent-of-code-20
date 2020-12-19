import time


def find_value(values: list[int], sum: int):
    for ind1, val1 in enumerate(values):
        for val2 in values[ind1 + 1:]:
            if val1 + val2 > sum:
                break
            if val1 + val2 == sum:
                return True
    return False


def p1(lines: list[int]):
    ind = 0
    span = 25
    while ind < len(lines) - span:
        past = lines[ind:ind + span]
        past.sort()
        next_num = lines[ind + span]
        if not find_value(past, next_num):
            print(f'p1 {next_num}')
            return next_num
        ind += 1
    raise RuntimeError('failed :(')


def p2(lines: list[int], invalid_num: int):

    min_ind = 0
    max_ind = min_ind + 2
    while min_ind < len(lines) - 1:
        section = lines[min_ind: max_ind]
        total = sum(section)
        if total == invalid_num:
            print(f'p2 {min(section) + max(section)}')
            return
        elif total < invalid_num:
            max_ind += 1
        else:
            min_ind += 1
            max_ind = min_ind + 2

    raise RuntimeError('failed :(')


def main():
    start = time.perf_counter()

    with open('./9/input.txt') as f:
        lines = f.readlines()

    lines = [int(x.rstrip()) for x in lines]

    invalid_num = p1(lines)
    p2(lines, invalid_num)

    end = time.perf_counter()
    print((end - start) * 1000)


if __name__ == '__main__':
    main()
