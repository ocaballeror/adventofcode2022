# type: ignore
import re

def read_input():
    with open("input") as f:
        return dict(line.strip().split(": ") for line in f)


def getp1(data, name):
    val = data[name]
    if val.isnumeric():
        return int(val)

    a, op, b = val.split()
    a = getp1(data, a)
    b = getp1(data, b)

    return int(eval(f'{a} {op} {b}'))


def getp2(data, name):
    if name == 'humn':
        return name
    val = data[name]
    if val.isnumeric():
        return int(val)

    a, op, b = val.split()
    a = getp2(data, a)
    b = getp2(data, b)

    if isinstance(a, int) and isinstance(b, int):
        return int(eval(f'{a} {op} {b}'))
    return a, op, b


def part1():
    data = read_input()
    return getp1(data, 'root')


def part2():
    data = read_input()

    a, _, b = getp2(data, "root")

    if 'humn' in str(a):
        target = b
        rem = a
    else:
        target = a
        rem = b

    while rem != 'humn':
        a, op, b = rem
        if 'humn' in str(a):
            rem, op, t = rem
            op = op.translate(op.maketrans('+*/-', '-/*+'))
            target = eval(f'{target} {op} {t}')
        else:
            t, op, rem = rem
            if op == '+':
                target = target - t
            elif op == '*':
                target = target / t
            elif op == '-':
                target = t - target
            elif op == '/':
                target = t / target

    return int(target)

if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
