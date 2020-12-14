import time
import re


def set_bits(mask: str, value: int):
    for ind, char in enumerate(mask[::-1]):
        if char == 'X':
            continue
        op = int(char)
        if op == 0:
            value &= ~(1 << ind)
        else:
            value |= (1 << ind)
    return value


def set_mask_bits(mask: str, value: str):
    mask_value = ""
    bit_string = f"{int(value):b}"
    bit_string = ("0" * (len(mask) - len(bit_string))) + bit_string
    for ind, char in enumerate(mask):
        if char == 'X':
            mask_value += char
        elif char == '0':
            mask_value += bit_string[ind]
        else:
            mask_value += '1'
    return mask_value


def p1(lines: list[str]):
    mem = {}
    cur_mask = ""
    pattern = re.compile(r'\[([0-9]*)\]')
    for line in lines:
        if line.startswith('mask = '):
            cur_mask = line.split('=')[1].strip()
        else:
            parts = line.split('=')
            offset = int(re.search(pattern, parts[0]).group(1))
            value = set_bits(cur_mask, int(parts[1]))
            mem[offset] = value

    print(sum(mem.values()))


def gen_masks(offset: str):
    values: list[str] = []
    x_ind = -1
    try:
        x_ind = offset.index('X')
    except ValueError:
        return [offset]

    bits = [offset[:x_ind]]

    for float_bit in ['0', '1']:
        sub_bits = gen_masks(float_bit + offset[x_ind + 1:])
        for bit in bits:
            for sub_bit in sub_bits:
                values.append(bit + sub_bit)

    return values


def p2(lines: list[str]):
    mem = {}
    cur_mask = ""
    pattern = re.compile(r'\[([0-9]*)\]')
    for line in lines:
        if line.startswith('mask = '):
            cur_mask = line.split('=')[1].strip()
        else:
            parts = line.split('=')
            offset = re.search(pattern, parts[0]).group(1)
            masked_offset = set_mask_bits(cur_mask, offset)
            value = int(parts[1])
            masks = gen_masks(masked_offset)
            for mask in masks:
                mem[int(mask, 2)] = value

    print(sum(mem.values()))


def main():
    start = time.perf_counter()

    with open('./14/input.txt') as f:
        lines = f.readlines()

    lines = [x.rstrip() for x in lines]

    p1(lines)
    p2(lines)

    end = time.perf_counter()
    print((end - start) * 1000)


if __name__ == "__main__":
    main()
