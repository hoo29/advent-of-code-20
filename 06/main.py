from typing import List
import time


def p1(answers: List[str]):
    count = 0
    group = set()
    for answer in answers:
        if answer == '':
            count += len(group)
            group = set()
        else:
            for char in answer:
                group.add(char)

    print(count)


def p2(answers: List[str]):
    count = 0
    group = []
    for answer in answers:
        person = set()
        if answer == '':
            all_yes = set.intersection(*group)
            count += len(all_yes)
            group = []
        else:
            for char in answer:
                person.add(char)
            group.append(person)

    print(count)


def main():
    start = time.perf_counter()

    with open('./6/input.txt') as f:
        answers = f.readlines()

    answers = [x.rstrip() for x in answers]
    answers.append('')

    p1(answers)
    p2(answers)

    end = time.perf_counter()
    print((end - start) * 1000)


if __name__ == "__main__":
    main()
