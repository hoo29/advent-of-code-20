import time


def sol(input: list[int], limit: int):
    ind = 0
    history: dict[int, list[int]] = {}
    last = -1
    # assume input content is unique
    while ind < limit:
        turn = ind + 1
        if ind < len(input):
            last = input[ind]
            history[last] = [turn]
        else:
            previous = history.get(last, None)
            if previous is None:
                raise RuntimeError('well this has gone badly')
            if len(previous) == 1:
                last = 0
            else:
                last = previous[1] - previous[0]
            last_prev = history.get(last, [])
            if len(last_prev) < 2:
                last_prev.append(turn)
            else:
                last_prev[0] = last_prev[1]
                last_prev[1] = turn
            history[last] = last_prev
        ind += 1
    print(last)


def main():
    start = time.perf_counter()

    input = [16, 1, 0, 18, 12, 14, 19]

    sol(input, 2020)
    sol(input, 30000000)

    end = time.perf_counter()
    print((end - start) * 1000)


if __name__ == '__main__':
    main()
