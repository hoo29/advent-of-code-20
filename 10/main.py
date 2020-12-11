import time


def p1(lines: list[int]):
    lines = lines.copy()

    lines.append(max(lines) + 3)
    count_1 = 0
    count_3 = 0
    previous = 0

    for ind in range(0, len(lines)):
        if lines[ind] - 1 == previous:
            count_1 += 1
        elif lines[ind] - 3 == previous:
            count_3 += 1
        else:
            raise RuntimeError('failed :(')
        previous = lines[ind]

    print(count_1 * count_3)


def p2(lines: list[int], cache: dict):

    # don't judge me
    lines_hash = "".join([str(x) for x in lines])

    if lines_hash in cache:
        return cache[lines_hash]

    if len(lines) == 1:
        return 1

    count = 0

    diffs = [lines.index(lines[0] + x)
             for x in range(1, 4) if lines[0] + x in lines]

    for diff in diffs:
        subset = lines[diff:]
        count += p2(subset, cache)

    cache[lines_hash] = cache.get(lines_hash, 0) + count

    return count


def main():
    start = time.perf_counter()

    with open('./10/input.txt') as f:
        lines = f.readlines()

    lines = [int(x.rstrip()) for x in lines]
    lines.sort()
    p1(lines)

    lines.insert(0, 0)
    res = p2(lines, {})
    print(res)
    end = time.perf_counter()
    print((end - start) * 1000)


if __name__ == "__main__":
    main()
