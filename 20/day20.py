# type: ignore

def read_input():
    with open("input") as f:
        return [int(line) for line in f if line.strip()]


def mix(data):
    for idx in range(len(data)):
        pos, elem = next(((i, val) for i, val in enumerate(data) if val[0] == idx))
        data.pop(pos)
        new = (pos + elem[1]) % len(data)
        data.insert(new, elem)

    return data


def value(data):
    zero = next((i for i, val in enumerate(data) if val[1] == 0))
    return data[(1000 + zero) % len(data)][1] + data[(2000 + zero) % len(data)][1] + data[(3000 + zero) % len(data)][1]


def part1():
    data = read_input()
    data = mix(list(enumerate(data)))
    return value(data)


def part2():
    data = read_input()
    data = list(enumerate(num * 811589153 for num in data))
    for _ in range(10):
        data = mix(data)

    return value(data)


if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
