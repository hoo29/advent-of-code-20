import time
import os
from typing import Union

Rule = Union[list[list[int]], str]
Rules = dict[int, Rule]


def parse_grammar(lines: list[str]):
    raw_rules = lines[:lines.index('')]
    rules: Rules = {}

    for rule in raw_rules:
        rule_ind = int(rule.split(':')[0])
        rule_content = rule.split(':')[1].lstrip()

        if '"' in rule_content:
            rules[rule_ind] = rule_content.replace('"', '')
        else:
            sub_rules_raw = rule_content.split('|')
            sub_rules: list[list[int]] = []
            for sub_rule in sub_rules_raw:
                parts = [int(x) for x in sub_rule.split()]
                sub_rules.append(parts)
            rules[rule_ind] = sub_rules

    return rules


def check_message2(rules: Rules, message: str, rules_to_proc: list[Union[int, str]]):
    # skeleton of this found after googling...

    if len(message) == 0 or len(rules_to_proc) == 0:
        return len(message) == 0 and len(rules_to_proc) == 0

    next_rule_raw = rules_to_proc.pop()

    if isinstance(next_rule_raw, str):
        if message[0] == next_rule_raw:
            return check_message2(rules, message[1:], rules_to_proc.copy())
    else:
        for sub_rule in rules[next_rule_raw]:
            if check_message2(rules, message, rules_to_proc + list(reversed(sub_rule))):
                return True

    return False


def check_message(rule: Rule, rules: Rules, message: str, message_ind: int):
    # pretty sure this works by chance...

    if message_ind >= len(message):
        return False, 0

    if isinstance(rule, str):
        return message[message_ind] == rule, message_ind + 1

    for sub_rules in rule:
        cur_message_ind = message_ind
        rule_match = True

        for sub_ind in sub_rules:

            valid, new_ind = check_message(
                rules[sub_ind], rules, message, cur_message_ind)
            if valid:
                cur_message_ind = new_ind
            else:
                rule_match = False
                break

        if rule_match:
            return True, cur_message_ind

    return False, 0


def p1(lines: list[str]):
    gram = parse_grammar(lines)
    messages = lines[lines.index('') + 1:]
    count = 0
    for message in messages:
        valid, match_count = check_message(
            gram[0], gram, message, 0)
        if valid and match_count == len(message):
            count += 1

    print(count)


def p2(lines: list[str]):
    gram = parse_grammar(lines)

    gram[8] = [[42], [42, 8]]
    gram[11] = [[42, 31], [42, 11, 31]]

    messages = lines[lines.index('') + 1:]
    count = len([x for x in messages if check_message2(gram,
                                                       x, list(reversed(gram[0][0])))])
    print(count)


def main():
    start = time.perf_counter()
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    with open(f'{cur_dir}/input.txt') as f:
        lines = f.readlines()

    lines = [x.rstrip() for x in lines]

    p1(lines)
    p2(lines)

    end = time.perf_counter()
    print((end - start) * 1000)


if __name__ == '__main__':
    main()
