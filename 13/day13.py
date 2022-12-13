from functools import cmp_to_key


def read_input():
    with open("input") as f:
        lines = f.read().splitlines()

    pairs = []
    for idx, line in enumerate(lines[::3]):
        pairs.append((eval(line), eval(lines[idx * 3 + 1])))

    return pairs


def compare(first, second):
    # print(f"Check {first} vs {second}")
    if isinstance(first, int) and isinstance(second, int):
        if first == second:
            return None
        return first < second

    if isinstance(first, int):
        first = [first]

    if isinstance(second, int):
        second = [second]

    for a, b in zip(first, second):
        if (c := compare(a, b)) is not None:
            return c

    if len(first) == len(second):
        return None
    return len(first) < len(second)


def part1():
    pairs = read_input()
    answ = 0
    for idx, (first, second) in enumerate(pairs):
        # print(f"Compare {first} vs {second}")
        if compare(first, second):
            answ += idx + 1

    return answ


def part2():
    pairs = read_input()
    pairs = [a for p in pairs for a in p]
    pairs.append([[2]])
    pairs.append([[6]])

    def key(a, b):
        c = compare(a, b)
        if c is True:
            return 1
        if c is False:
            return -1
        return 0

    pairs.sort(key=cmp_to_key(key), reverse=True)

    return (pairs.index([[2]]) + 1) * (pairs.index([[6]]) + 1)


if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
