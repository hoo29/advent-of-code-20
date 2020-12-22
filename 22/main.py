import time
import os


def load_cards(lines: list[str]):
    player_1_raw = lines[1:lines.index('')]
    player1: list[int] = [int(x) for x in player_1_raw]

    player_2_raw = lines[lines.index('') + 2:]
    player2: list[int] = [int(x) for x in player_2_raw]

    return player1, player2


def p1(lines: list[str]):
    player1, player2 = load_cards(lines)
    while len(player1) > 0 and len(player2) > 0:
        if player1[0] == player2[0]:
            raise RuntimeError('not sure what happens on a draw')
        elif player1[0] > player2[0]:
            player1.append(player1[0])
            player1.append(player2[0])
        else:
            player2.append(player2[0])
            player2.append(player1[0])
        player1.pop(0)
        player2.pop(0)

    winner = player1 if len(player1) > 0 else player2
    winner.reverse()
    count = 0
    for ind, value in enumerate(winner):
        count += (ind + 1) * value

    print(count)


def recurse_combat(player1: list[int], player2: list[int]):
    p1_hist: list[list[int]] = []
    p2_hist: list[list[int]] = []
    winner = False
    while len(player1) > 0 and len(player2) > 0:
        if player1 in p1_hist and player2 in p2_hist:
            return True

        p1_hist.append(player1.copy())
        p2_hist.append(player2.copy())

        if player1[0] == player2[0]:
            raise RuntimeError('not sure what happens on a draw')
        elif player1[0] <= len(player1) - 1 and player2[0] <= len(player2) - 1:
            winner = recurse_combat(player1[1:player1[0] + 1], player2[1:player2[0] + 1])
        elif player1[0] > player2[0]:
            winner = True
        else:
            winner = False

        if winner:
            player1.append(player1[0])
            player1.append(player2[0])
        else:
            player2.append(player2[0])
            player2.append(player1[0])

        player1.pop(0)
        player2.pop(0)

    return len(player2) == 0


def p2(lines: list[str]):
    player1, player2 = load_cards(lines)
    recurse_combat(player1, player2)
    winner = player1 if len(player1) > 0 else player2
    winner.reverse()
    count = 0
    for ind, value in enumerate(winner):
        count += (ind + 1) * value

    print(count)


def main():
    start = time.perf_counter()

    with open(f'{os.path.dirname(os.path.realpath(__file__))}/input.txt') as f:
        lines = f.readlines()

    lines = [x.rstrip() for x in lines]

    p1(lines)
    p2(lines)

    end = time.perf_counter()
    print((end - start) * 1000)


if __name__ == '__main__':
    main()
