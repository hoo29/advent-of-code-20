from __future__ import annotations
from typing import List
import time


class Bag:
    def __init__(self, colour: str, style: str, edges: dict[Bag, int]) -> None:
        super().__init__()
        self._colour: str = colour
        self._style: str = style
        self.edges = edges
        self.parents: set[Bag] = set()

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Bag):
            return NotImplemented

        return o.colour == self.colour and o.style == self.style

    def __hash__(self) -> int:
        return hash(f'{self.colour}{self.style}')

    @property
    def colour(self):
        return self._colour

    @property
    def style(self):
        return self._style

    def add_edge(self, bag: Bag, count: int) -> None:
        existing = self.edges.get(bag)
        if existing is None:
            bag.add_parent(self)
            self.edges[bag] = count
        else:
            self.edges[bag] += count

    def add_parent(self, bag: Bag) -> None:
        self.parents.add(bag)


def search_parents(parents: set[Bag], bag_to_match: Bag, visited: set[Bag]):
    for node in parents:
        if node not in visited:
            visited.add(node)
            search_parents(node.parents, bag_to_match, visited)


def parse_bag(tree: list[Bag], item: str) -> Bag:
    if item.endswith('.'):
        item = item[:-1]
    bag_details = item.split()
    bag_style = bag_details[0]
    bag_colour = bag_details[1]
    bag = Bag(bag_colour, bag_style, {})

    try:
        existing = tree.index(bag)
    except ValueError:
        existing = None

    if existing is None:
        tree.append(bag)
    else:
        bag = tree[existing]

    return bag


def parse_edge(tree: list[Bag], item: str):
    if 'no other bags' in item:
        return None

    details = item.split(None, 1)
    count = int(details[0])

    bag = parse_bag(tree, details[1])

    return {'bag': bag, 'count': count}


def make_tree(rules: List[str]):
    tree: list[Bag] = []
    for rule in rules:
        items = rule.split('contain')
        bag = parse_bag(tree, items[0])
        edge_details = items[1].split(',')

        for edge in edge_details:
            edge_details = parse_edge(tree, edge)
            if edge_details is not None:
                bag.add_edge(edge_details['bag'], edge_details['count'])

    return tree


def p1(tree: list[Bag]):

    the_bag = parse_bag(tree, 'shiny gold bag')
    count = set()
    search_parents(the_bag.parents, the_bag, count)

    print(len(count))


def count_children(bag: Bag):
    count = 0
    for child_bag, child_count in bag.edges.items():
        count += child_count
        count += child_count * count_children(child_bag)

    return count


def p2(tree: list[Bag]):
    the_bag = parse_bag(tree, 'shiny gold bag')
    count = count_children(the_bag)

    print(count)


def main():
    start = time.perf_counter()

    with open('./7/input.txt') as f:
        rules = f.readlines()

    rules = [x.rstrip() for x in rules]
    tree = make_tree(rules)

    p1(tree)
    p2(tree)

    end = time.perf_counter()
    print((end - start) * 1000)


if __name__ == '__main__':
    main()
