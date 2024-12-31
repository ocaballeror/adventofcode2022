# type: ignore
import itertools
from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int

    def __add__(self, other):
        return Point(x=self.x + other.x, y=self.y + other.y)

    def as_tuple(self):
        return self.x, self.y


@dataclass
class Rock:
    points: tuple[Point]

    def create(self, rocks):
        hi = max(p[1] for p in rocks) if rocks else -1
        return Rock(tuple(p + Point(2, hi + 4) for p in self.points))

    def move(self, to):
        if to == 'v':
            move = Point(0, -1)  # y is 0 at floor. rocks go up
        elif to == '>':
            move = Point(1, 0)
        elif to == '<':
            move = Point(-1, 0)

        new = [p + move for p in self.points]
        if any(p.x < 0 or p.x > 6 for p in new):
            return self

        return Rock(tuple(new))


def read_input():
    with open("input") as f:
        return list(f.read().strip())


def draw():
    for rock in sorted((r[1], r[0]) for r in rocks):
        pass


def part1():
    defrocks = itertools.cycle([
        Rock((Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0))),
        Rock((Point(1, 0), Point(0, 1), Point(1, 1), Point(2, 1), Point(1, 2))),
        Rock((Point(0, 0), Point(1, 0), Point(2, 0), Point(2, 1), Point(2, 2))),
        Rock((Point(0, 0), Point(0, 1), Point(0, 2), Point(0, 3))),
        Rock((Point(0, 0), Point(0, 1), Point(1, 0), Point(1, 1))),
    ])
    jets = itertools.cycle(read_input())
    rocks = set()

    for it in range(5):
        print(it)
        new = next(defrocks).create(rocks)

        while True:
            new = new.move(next(jets))
            moved = new.move('v')
            if any(p.y < 0 or p.as_tuple() in rocks for p in moved.points):
                break
            new = moved

        rocks.update(p.as_tuple() for p in new.points)

    print(rocks)
    return max(p[1] for p in rocks)


def part2():
    data = read_input()


if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
