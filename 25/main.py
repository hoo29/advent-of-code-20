import time


def hack_loop_size(subject_num: int, public_key: int, values_to_ignore: list[int]):
    subject_val = 1
    loop_size = 0
    while True:
        subject_val *= subject_num
        subject_val %= 20201227
        loop_size += 1
        if subject_val == public_key and subject_val not in values_to_ignore:
            return subject_val, loop_size


def transform(loop_size: int, subject_num: int):
    subject_val = 1
    for _ in range(loop_size):
        subject_val *= subject_num
        subject_val %= 20201227
    return subject_val


def p1():
    card_pub_key = 10441485
    door_pub_key = 1004920

    card_subject_num = 7
    door_subject_num = 7
    print('hack commencing')

    card_subject_num, card_loop_size = hack_loop_size(card_subject_num, card_pub_key, [])
    print(f'card loop size {card_loop_size}')

    door_subject_num, door_loop_size = hack_loop_size(door_subject_num, door_pub_key, [card_loop_size])
    print(f'door loop size {door_loop_size}')

    enc_key = transform(card_loop_size, door_subject_num)
    enc_key2 = transform(door_loop_size, card_subject_num)

    if enc_key != enc_key2:
        raise RuntimeError('something has gone wrong')

    print(f'hacked {enc_key}')


def main():
    start = time.perf_counter()

    p1()

    end = time.perf_counter()
    print((end - start) * 1000)


if __name__ == '__main__':
    main()
