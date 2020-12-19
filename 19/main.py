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

# pretty sure this works by chance...


def check_message(rule: Rule, rules: Rules, message: str, message_ind: int):

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


# skeleton of this found after googling...

def check_message_but_better(message: str, rule_stack: list[Union[int, str]], rules: Rules):
    if len(rule_stack) > len(message):
        return False
    elif len(rule_stack) == 0 or len(message) == 0:
        return len(rule_stack) == 0 and len(message) == 0

    rule_ind_raw = rule_stack.pop()
    if isinstance(rule_ind_raw, str):
        if message[0] == rule_ind_raw:
            return check_message_but_better(message[1:], rule_stack.copy(), rules)
    else:
        for sub_rule in rules[rule_ind_raw]:
            if check_message_but_better(message, rule_stack + list(reversed(sub_rule)), rules):
                return True

    return False


def p2(lines: list[str]):
    gram = parse_grammar(lines)

    gram[8] = [[42], [42, 8]]
    gram[11] = [[42, 31], [42, 11, 31]]

    messages = lines[lines.index('') + 1:]
    count = len([x for x in messages if check_message_but_better(
        x, list(reversed(gram[0][0])), gram)])

    print(count)


def main():
    start = time.perf_counter()
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    with open(f'{cur_dir}/test1.txt') as f:
        lines = f.readlines()

    lines = [x.rstrip() for x in lines]

    p1(lines)
    p2(lines)

    end = time.perf_counter()
    print((end - start) * 1000)


if __name__ == '__main__':
    main()
