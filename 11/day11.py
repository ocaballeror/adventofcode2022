# type: ignore
import re
import math


def read_input():
    with open("input") as f:
        data = [[part.strip() for part in monk.split("\n")] for monk in f.read().split("\n\n")]

    monkeys = []
    for idx, group in enumerate(data):
        items = list(map(int, re.findall(r"\d+", group[1])))
        op = eval(group[2].replace("Operation: new =", "lambda old:"))
        div = int(group[3].split()[-1])
        first = int(group[4].split()[-1])
        second = int(group[5].split()[-1])

        monkeys.append((items, op, (first, second, div)))

    return monkeys


def part1():
    monkeys = read_input()
    counts = [0] * len(monkeys)
    for roundnr in range(20):
        for idx, (items, op, (first, second, div)) in enumerate(monkeys):
            counts[idx] += len(items)
            for it in items:
                it = op(it) // 3
                passto = first if it % div == 0 else second
                if passto == idx:
                    raise ValueError("wtf")
                monkeys[passto][0].append(it)
            items.clear()

    counts.sort(reverse=True)
    return counts[0] * counts[1]


def part2():
    monkeys = read_input()
    counts = [0] * len(monkeys)
    common = math.lcm(*(m[2][2] for m in monkeys))
    for roundnr in range(10000):
        for idx, (items, op, (first, second, div)) in enumerate(monkeys):
            counts[idx] += len(items)
            for it in items:
                it = op(it) % common
                passto = first if it % div == 0 else second
                monkeys[passto][0].append(it)
            items.clear()

    counts.sort(reverse=True)
    return counts[0] * counts[1]


if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
