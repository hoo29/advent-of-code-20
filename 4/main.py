from typing import List, Dict, Callable, Tuple
import time
import re


def p1(passports: List[str]):
    count = 0

    pattern = re.compile(r'([a-z]{3})\:')
    required = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

    current_passport = []
    for line in passports:
        if line == '':
            if all(x in current_passport for x in required):
                count += 1
            current_passport = []
        else:
            matches = re.findall(pattern, line)
            current_passport += matches

    print(count)


def check_height(height: str):
    limits = {
        "cm": [150, 193],
        "in": [59, 76]
    }

    if len(height) < 3:
        return False

    unit = height[-2:]

    if unit not in limits.keys():
        return False

    measurement = int(height[:-2])

    return measurement >= limits[unit][0] and measurement <= limits[unit][1]


def check_passport(current_passport: dict[str, str]):
    required: dict[str, Callable[[str], bool]] = {
        'byr': lambda x: len(x) == 4 and int(x) >= 1920 and int(x) <= 2002,
        'iyr': lambda x: len(x) == 4 and int(x) >= 2010 and int(x) <= 2020,
        'eyr': lambda x: len(x) == 4 and int(x) >= 2020 and int(x) <= 2030,
        'hgt': check_height,
        'hcl': lambda x: re.fullmatch(r'#[a-f0-9]{6}', x),
        'ecl': lambda x: x in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'],
        'pid': lambda x: re.fullmatch(r'[0-9]{9}', x)
    }

    for key, value in required.items():
        if key not in current_passport.keys():
            return False
        if not value(current_passport[key]):
            return False

    return True


def p2(passports: List[str]):
    count = 0

    pattern = re.compile(r'([a-z]{3})\:([^\s]*)')

    current_passport = {}
    for line in passports:
        if line == '':
            if check_passport(current_passport):
                count += 1
            current_passport = {}
        else:
            matches = re.findall(pattern, line)
            current_passport = {**current_passport, **
                                {item[0]: item[1] for item in matches}}

    print(count)


def main():
    start = time.perf_counter()

    with open('./4/input.txt') as f:
        passports = f.readlines()

    # make sure we get the last one
    passports.append('')

    passports = [x.rstrip() for x in passports]

    p1(passports)
    p2(passports)

    end = time.perf_counter()
    print((end - start) * 1000)


if __name__ == "__main__":
    main()
