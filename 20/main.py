import time
import os
import math
from enum import IntEnum

Tiles = list[list[list[str]]]


class Mod(IntEnum):
    N_O = 0
    # flipped vertically
    N_F = 1
    E_O = 2
    E_F = 3
    S_O = 4
    S_F = 5
    W_O = 6
    W_F = 7


def flip_v(tile: list[str]):
    return tile[::-1]


def rotate_90(tile: list[str]):
    rotated: list[str] = []
    for x in range(len(tile)):
        line = ''.join([tile[y_ind][x] for y_ind in range(len(tile))])
        rotated.append(line[::-1])

    return rotated


class Tile:
    def __init__(self, raw: list[str], modi: Mod, tile_id: int) -> None:
        super().__init__()
        self.raw = raw
        self.calc_edges(raw)
        top, right, bottom, left = self.calc_edges(raw)
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left
        self._modi = modi
        self._tile_id = tile_id
        self.matched_edges = -1
        self.maybe_tops: list[Tile] = []
        self.maybe_rights: list[Tile] = []
        self.maybe_bottoms: list[Tile] = []
        self.maybe_lefts: list[Tile] = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Tile):
            return NotImplemented

        return o.tile_id == self.tile_id and o.modi == self.modi

    def __hash__(self) -> int:
        return hash(f'{self.tile_id}{self.modi}')

    @property
    def tile_id(self):
        return self._tile_id

    @property
    def modi(self):
        return self._modi

    def pretty_print(self):
        for line in self.raw:
            print(line)
        print()

    def calc_edges(self, raw: list[str]):
        top = int(raw[0].replace('.', '0').replace('#', '1'), 2)
        bottom = int(raw[-1].replace('.', '0').replace('#', '1'), 2)
        left = int(''.join([raw[y_ind][0] for y_ind in range(len(raw))]).replace('.', '0').replace('#', '1'), 2)
        right = int(''.join([raw[y_ind][-1] for y_ind in range(len(raw))]).replace('.', '0').replace('#', '1'), 2)
        return top, right, bottom, left


def load_tiles(lines: list[str]):
    array_size = int(math.sqrt(lines.count('')))
    tiles: dict[int, list[Tile]] = {}

    raw_lines = lines.copy()

    for ind in range(array_size ** 2):

        raw_tile = raw_lines[:raw_lines.index('')]
        tile_id = int(raw_tile[0].split(' ')[1][:-1])
        tile_content = raw_tile[1:]

        tiles[tile_id] = []
        for dir_ in range(4):
            tile_cp = tile_content.copy()
            for _ in range(dir_):
                tile_cp = rotate_90(tile_cp)
            tile_1 = Tile(tile_cp, list(Mod)[dir_], tile_id)
            tile_cp = flip_v(tile_cp)
            tile_2 = Tile(tile_cp, list(Mod)[dir_ + 1], tile_id)
            tiles[tile_id].append(tile_1)
            tiles[tile_id].append(tile_2)

        raw_lines = raw_lines[raw_lines.index('') + 1:]
        ind += 1

    return tiles


def p1(lines: list[str]):
    tiles = load_tiles(lines)

    for_p1: set[int] = set()
    corners: list[Tile] = []
    edges: list[Tile] = []
    centres: list[Tile] = []
    for tile_id, tile_mods in tiles.items():
        temp_dict = tiles.copy()
        temp_dict.pop(tile_id)

        for tile in tile_mods:
            edges_to_match = {'top', 'bottom', 'right', 'left'}
            for _, other_tiles_mods in temp_dict.items():
                for other_tile in other_tiles_mods:
                    if tile.top == other_tile.bottom:
                        edges_to_match.remove('top')
                        tile.maybe_tops.append(other_tile)

                    if tile.bottom == other_tile.top:
                        edges_to_match.remove('bottom')
                        tile.maybe_bottoms.append(other_tile)

                    if tile.left == other_tile.right:
                        edges_to_match.remove('left')
                        tile.maybe_lefts.append(other_tile)

                    if tile.right == other_tile.left:
                        edges_to_match.remove('right')
                        tile.maybe_rights.append(other_tile)
            tile.matched_edges = 4 - len(edges_to_match)

            if tile.matched_edges == 2:
                corners.append(tile)
                for_p1.add(tile_id)
            elif tile.matched_edges == 3:
                edges.append(tile)
            elif tile.matched_edges == 4:
                centres.append(tile)

    print(math.prod(list(for_p1)))

    return tiles, corners, edges, centres


def solve(grid_size: int, ind: int, used: list[Tile]):

    x_ind = ind % grid_size
    y_ind = ind // grid_size

    cur = used[-1]

    if y_ind > 0 and x_ind > 0:
        top_tile = used[-(grid_size + 1)]
        if top_tile not in cur.maybe_tops:
            return False, []

    if len(used) == grid_size ** 2:
        return True, used

    if x_ind < grid_size - 1:
        for next_ in cur.maybe_rights:
            if next_ in used:
                continue
            found, history = solve(grid_size, ind + 1, used.copy() + [next_])
            if found:
                return True, history
    # start a new line
    if x_ind == grid_size - 1:
        prev_first = used[-grid_size]
        for next_ in prev_first.maybe_bottoms:
            if next_ in used:
                continue
            found, history = solve(grid_size, ind + 1, used.copy() + [next_])
            if found:
                return True, history

    return False, []


def draw_the_rest_of_the_owl(grid_size: int, corners: list[Tile]):

    starters = [x for x in corners if len(x.maybe_rights) > 0 and len(x.maybe_bottoms) > 0]
    for corner in starters:
        found, history = solve(grid_size, 0, [corner])
        if found:
            return True, history

    return False, []


def check_lines_for_monster(monster: list[list[int]], picture: list[str], y_ind: int, x_ind: int):
    for check in monster[0]:
        if picture[y_ind][x_ind + check] != '#':
            return False
        for check in monster[1]:
            if picture[y_ind + 1][x_ind + check] != '#':
                return False
        for check in monster[2]:
            if picture[y_ind + 2][x_ind + check] != '#':
                return False
    return True


def find_the_monster(history: list[Tile], array_size: int):
    trimmed_size = len(history[0].raw) - 2
    picture: list[str] = [''] * (array_size * trimmed_size)
    ind = 0
    for tile in history:
        trimmed = tile.raw[1:-1]
        trimmed = [trimmed[y_ind][1:-1] for y_ind in range(len(trimmed))]
        y_ind = ind // array_size
        for yy_ind, yy in enumerate(range(y_ind * trimmed_size, (y_ind + 1) * trimmed_size)):
            picture[yy] += trimmed[yy_ind]
        ind += 1

    monster = [[18], [0, 5, 6, 11, 12, 17, 18, 19], [1, 4, 7, 10, 13, 16]]

    pictures_to_try: list[list[str]] = []
    for dir_ in range(4):
        picture_cp = picture.copy()
        for _ in range(dir_):
            picture_cp = rotate_90(picture_cp)
        pictures_to_try.append(picture_cp)
        picture_cp = flip_v(picture_cp)
        pictures_to_try.append(picture_cp)

    for plz in pictures_to_try:
        monster_count = 0
        # assume monsters aren't overlapping
        for y_ind in range(0, (array_size * trimmed_size) - 3):
            for x_ind in range((array_size * trimmed_size) - 19):

                if check_lines_for_monster(monster, plz, y_ind, x_ind):
                    monster_count += 1

        if monster_count > 0:
            hash_count = 0
            for line in plz:
                hash_count += line.count('#')
            monster_hash_sum = 0
            for m in monster:
                monster_hash_sum += len(m)
            hash_count -= monster_hash_sum * monster_count

            print(hash_count)


def main():
    start = time.perf_counter()

    with open(f'{os.path.dirname(os.path.realpath(__file__))}/input.txt') as f:
        lines = f.readlines()

    lines = [x.rstrip() for x in lines]
    if lines[-1] != '':
        lines.append('')

    array_size = int(math.sqrt(lines.count('')))
    _, corners, _, _ = p1(lines)

    found, history = draw_the_rest_of_the_owl(array_size, corners)
    if not found:
        raise RuntimeError('wut')
    find_the_monster(history, array_size)
    end = time.perf_counter()
    print((end - start) * 1000)


if __name__ == '__main__':
    main()
