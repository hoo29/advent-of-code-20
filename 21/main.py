import time
import os
import copy


def parse_ingredients(lines: list[str]):
    all_words: set[str] = set()
    all_allergens: dict[str, list[set[str]]] = {}
    all_lists: list[set[str]] = []

    for line in lines:
        list_ = set(line[:line.index('(') - 1].split())
        allergens = line[line.index('(') + 10:-1].replace(' ', '').split(',')
        all_words = all_words.union(list_)
        all_lists.append(list_)
        for allergen in allergens:
            existing = all_allergens.get(allergen, [])
            existing.append(list_)
            all_allergens[allergen] = existing

    return all_allergens, all_words, all_lists


def remove_word_from_allergens(all_allergens: dict[str, list[set[str]]], word: str):
    for _, words in all_allergens.items():
        for list_ in words:
            list_.discard(word)


def found_one(all_allergens: dict[str, list[set[str]]], all_words: set[str], solved: dict[str, str], the_word: str, allergen: str):
    solved[allergen] = the_word
    all_words.remove(the_word)
    all_allergens.pop(allergen)
    remove_word_from_allergens(all_allergens, the_word)


def solve(all_allergens: dict[str, list[set[str]]], all_words: set[str], solved: dict[str, str]):

    all_allergens_cp = copy.deepcopy(all_allergens)

    while len(all_allergens_cp) > 0:
        changed = False
        all_allergens_temp = all_allergens_cp.copy()
        for allergen, words in all_allergens_cp.items():
            if len(words) > 1:
                result = set.intersection(*words)
                if len(result) == 1:
                    the_word = list(result)[0]
                    found_one(all_allergens_temp, all_words, solved, the_word, allergen)
                    changed = True
            elif len(words[0]) == 1:
                the_word = list(words[0])[0]
                found_one(all_allergens_temp, all_words, solved, the_word, allergen)
                changed = True
        if not changed:
            raise RuntimeError('cannot solve more')
        all_allergens_cp = all_allergens_temp


def p1(lines: list[str]):
    all_allergens, all_words, all_lists = parse_ingredients(lines)
    solved: dict[str, str] = {}
    solve(all_allergens, all_words, solved)
    count = 0
    for list_ in all_lists:
        for word in all_words:
            if word in list_:
                count += 1

    print(count)
    return solved


def p2(solved: dict[str, str]):
    results = list(solved.items())
    results.sort(key=lambda thing: thing[0])

    danger_list = [x[1] for x in results]
    print(','.join(danger_list))


def main():
    start = time.perf_counter()

    with open(f'{os.path.dirname(os.path.realpath(__file__))}/input.txt') as f:
        lines = f.readlines()

    lines = [x.rstrip() for x in lines]

    solved = p1(lines)
    p2(solved)

    end = time.perf_counter()
    print((end - start) * 1000)


if __name__ == '__main__':
    main()
