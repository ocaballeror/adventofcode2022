import itertools

from dataclasses import dataclass


@dataclass(unsafe_hash=True, frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other):
        other = Point(*other)
        return Point(x=self.x + other.x, y=self.y + other.y)

    def as_tuple(self):
        return self.x, self.y


def parse_input():
    with open("input") as f:
        content = f.read().splitlines()

    rocks = set()
    for line in content:
        parts = line.strip().split(" -> ")
        for idx, coord in enumerate(parts[1:]):
            a, b = map(int, parts[idx].split(','))
            c, d = map(int, coord.split(','))
            a, c = (a, c) if c >= a else (c, a)
            b, d = (b, d) if d >= b else (d, b)
            for point in itertools.product(range(a, c + 1), range(b, d + 1)):
                rocks.add(Point(*point))

    return rocks


def part1():
    rocks = parse_input()
    sand = set()
    void = max(r.y for r in rocks)

    grain = Point(500, 0)
    while True:
        if grain.y >= void:
            return len(sand)
        for move in [(0, 1), (-1, 1), (1, 1)]:
            other = grain + move
            if other not in rocks and other not in sand:
                grain = other
                break
        else:
            sand.add(grain)
            grain = Point(500, 0)


def part2():
    rocks = parse_input()
    sand = set()
    floor = max(r.y for r in rocks) + 2

    grain = Point(500, 0)
    while True:
        for move in [(0, 1), (-1, 1), (1, 1)]:
            other = grain + move
            if other not in rocks and other not in sand and other.y < floor:
                grain = other
                break
        else:
            sand.add(grain)
            if grain == Point(500, 0):
                return len(sand)
            grain = Point(500, 0)


if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
