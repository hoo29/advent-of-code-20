import time
from typing import Union


def p1(pinput: list[int]):
    moves = 100
    cups = pinput.copy()
    cur_cup_ind = 0
    for ind in range(moves):
        cur_cup_ind = ind % len(cups)
        cur_cup = cups[cur_cup_ind]
        picked_up_cups: list[int] = []

        for pick_ind in range(3):
            picked_up_cups.append(cups[(cur_cup_ind + 1 + pick_ind) % len(cups)])
        for pick_ind in range(3):
            if cur_cup_ind + 1 < len(cups):
                cups.pop(cur_cup_ind + 1)
            else:
                cups.pop(0)

        dest_num = cur_cup - 1

        if dest_num < min(cups):
            dest_num = max(cups)

        while dest_num not in cups:
            dest_num -= 1
            if dest_num < 0:
                raise RuntimeError('something has gone wrong')

        dest_ind = cups.index(dest_num)

        cups: list[int] = cups[:dest_ind + 1] + picked_up_cups + cups[dest_ind + 1:]
        while cups.index(cur_cup) != cur_cup_ind:
            cups.append(cups.pop(0))

    cur_cup_ind = (cur_cup_ind + 1) % len(cups)

    print()
    one_ind = (cups.index(1) + 1) % len(cups)
    final = ''
    for i in range(len(cups) - 1):
        final += str(cups[(one_ind + i) % len(cups)])
        print(cups[(one_ind + i) % len(cups)], end='')
    print()
    print()


class LL:
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value: int = value
        self.next: LL


def p2(pinput: list[int]):
    moves = 10000000

    cups: dict[int, LL] = {}
    last: Union[LL, None] = None

    for x in pinput:
        cur = LL(x)
        if isinstance(last, LL):
            last.next = cur
        last = cur
        cups[x] = cur

    for x in range(max(cups) + 1, 1000001):
        cur = LL(x)
        if isinstance(last, LL):
            last.next = cur
        last = cur
        cups[x] = cur

    cur_cup = cups[pinput[0]]
    last.next = cur_cup
    max_ = len(cups)

    for ind in range(moves):
        if ind % 1000000 == 0:
            print(ind)
        n1 = cur_cup.next
        n2 = n1.next
        n3 = n2.next

        cur_cup.next = n3.next
        dest_value = cur_cup.value - 1 if cur_cup.value - 1 > 0 else max_
        while dest_value in [n1.value, n2.value, n3.value]:
            dest_value = dest_value - 1 if dest_value - 1 > 0 else max_

        dest_cup = cups[dest_value]
        n3.next = dest_cup.next
        dest_cup.next = n1
        cur_cup = cur_cup.next

    print()
    one_cup = cups[1]
    c1 = one_cup.next
    c2 = c1.next

    print(c1.value * c2.value)
    print()


def main():
    start = time.perf_counter()

    pinput = [int(x) for x in '792845136']

    p1(pinput)
    p2(pinput)

    end = time.perf_counter()
    print((end - start) * 1000)


if __name__ == '__main__':
    main()
