import time


def p1(program: list[str]):
    acc = 0
    line_num = 0
    run_lines = set()
    while line_num < len(program):
        run_lines.add(line_num)
        operator = program[line_num].split()[0]
        operand = program[line_num].split()[1]

        if operator == 'acc':
            acc += int(operand)
            line_num += 1
        elif operator == 'jmp':
            line_num += int(operand)
        elif operator == 'nop':
            line_num += 1
        else:
            raise RuntimeError(f'unknown op {operator}')

        if line_num in run_lines:
            print(f'loop, acc {acc}')
            return


def p2(program: list[str]):
    acc = 0
    line_num = 0

    run_lines = set()
    switched_lines = set()
    switched = False

    while True:
        run_lines.add(line_num)
        operator = program[line_num].split()[0]
        operand = program[line_num].split()[1]

        if not switched and line_num not in switched_lines and operator in ['jmp', 'nop']:
            if operator == 'jmp':
                operator = 'nop'
            elif operator == 'nop':
                operator = 'jmp'
            switched_lines.add(line_num)
            switched = True

        if operator == 'acc':
            acc += int(operand)
            line_num += 1
        elif operator == 'jmp':
            line_num += int(operand)
        elif operator == 'nop':
            line_num += 1
        else:
            raise RuntimeError(f'unknown op {operator}')

        if line_num in run_lines:
            if not switched:
                raise RuntimeError(
                    'switched them all and it is still broken :(')
            switched = False
            acc = 0
            line_num = 0
            run_lines = set()
            continue

        if line_num == len(program):
            print(f'fixed, acc {acc}')
            return


def main():
    start = time.perf_counter()

    with open('./8/input.txt') as f:
        program = f.readlines()

    program = [x.rstrip() for x in program]

    p1(program)
    p2(program)

    end = time.perf_counter()
    print((end - start) * 1000)


if __name__ == '__main__':
    main()
