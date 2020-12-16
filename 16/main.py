import time
import math


def parse_rules(lines: list[str]):
    rules: dict[str, tuple[int, int]] = {}
    raw_rules = lines[:lines.index('')]
    for raw_rule in raw_rules:
        name = raw_rule.split(':')[0]
        raw_bounds = raw_rule.split(':')[1].split('or')
        bounds = []
        for raw_bound in raw_bounds:
            bounds.append(
                (int(raw_bound.split('-')[0]), int(raw_bound.split('-')[1])))
        rules[name] = bounds

    return rules


def parse_my_ticket(lines: list[str]):
    my_ticket = lines[lines.index('your ticket:') + 1]
    items = [int(x) for x in my_ticket.split(',')]

    return items


def parse_nearby_tickets(lines: list[str]):
    nearby_tickets = lines[lines.index('nearby tickets:') + 1:]
    items = []
    for nearby_ticket in nearby_tickets:
        items.append([int(x) for x in nearby_ticket.split(',')])

    return items


def check_value_valid_for_rule(value: int, rule_bounds: tuple[int, int]):
    for bound in rule_bounds:
        if bound[0] <= value <= bound[1]:
            return True
    return False


def check_value_valid(value: int, rules: dict[str, tuple[int, int]]):
    for _, rule_bounds in rules.items():
        if check_value_valid_for_rule(value, rule_bounds):
            return True
    return False


def check_ticket_valid(ticket: list[int], rules: dict[str, tuple[int, int]]):
    for value in ticket:
        match = check_value_valid(value, rules)
        if not match:
            return False
    return True


def p1(lines: list[str]):
    rules = parse_rules(lines)
    nearby_tickets = parse_nearby_tickets(lines)

    count = [value for ticket in nearby_tickets for value in ticket if not check_value_valid(
        value, rules)]
    print(sum(count))


def p2(lines: list[str]):
    rules = parse_rules(lines)
    nearby_tickets = parse_nearby_tickets(lines)
    valid_nearby_tickets = [
        ticket for ticket in nearby_tickets if check_ticket_valid(ticket, rules)]
    my_ticket = parse_my_ticket(lines)

    maybe = [set() for _ in valid_nearby_tickets[0]]
    no = [set() for _ in valid_nearby_tickets[0]]

    for ticket in valid_nearby_tickets:
        for value_ind, value in enumerate(ticket):
            for rule_name, rule_bounds in rules.items():
                if check_value_valid_for_rule(value, rule_bounds):
                    if rule_name not in no[value_ind]:
                        maybe[value_ind].add(rule_name)
                else:
                    no[value_ind].add(rule_name)
                    maybe[value_ind].discard(rule_name)

    done = False
    while not done:
        changed = False
        for set_with_one_element_ind in [x for x in range(0, len(maybe)) if len(maybe[x]) == 1]:
            set_with_one_element = maybe[set_with_one_element_ind]
            for other_set_ind in [x for x in range(0, len(maybe)) if x != set_with_one_element_ind and len(maybe[x]) != 1]:
                changed = True
                maybe[other_set_ind] = maybe[other_set_ind].difference(
                    set_with_one_element)
        if not changed:
            done = True

    solved: list[str] = [list(x)[0] for x in maybe]

    count = [my_ticket[ind]
             for ind, name in enumerate(solved) if name.startswith('departure')]

    print(math.prod(count))


def main():
    start = time.perf_counter()

    with open('./16/input.txt') as f:
        lines = f.readlines()

    lines = [x.rstrip() for x in lines]

    p1(lines)
    p2(lines)

    end = time.perf_counter()
    print((end - start) * 1000)


if __name__ == "__main__":
    main()
