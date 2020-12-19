from typing import List
import time


def p1(passwords: List[str]):
    matches = 0
    for item in passwords:
        parts = item.split(' ')
        req = parts[0]
        char = parts[1][:-1]
        password = parts[2]

        min_items = int(req.split('-')[0])
        max_items = int(req.split('-')[1])

        count = password.count(char)
        if count >= min_items and count <= max_items:
            matches += 1

    print(matches)


def p2(passwords: List[str]):
    matches = 0
    for item in passwords:
        parts = item.split(' ')
        req = parts[0]
        char = parts[1][:-1]
        password = parts[2]

        pos1 = int(req.split('-')[0])
        pos2 = int(req.split('-')[1])

        match1 = password[pos1 - 1] == char
        match2 = password[pos2 - 1] == char

        if match1 ^ match2:
            matches += 1

    print(matches)


if __name__ == '__main__':
    start = time.perf_counter()

    with open('./2/input.txt') as f:
        passwords = f.readlines()

    # take off \n
    passwords = [x.rstrip() for x in passwords]

    p1(passwords)
    p2(passwords)

    end = time.perf_counter()
    print((end - start) * 1000)
