# type: ignore
import os
import time
import itertools
from dataclasses import dataclass

try:
    from tqdm import tqdm, trange
except ImportError:
    tqdm = iter
    trange = range


@dataclass(frozen=True, unsafe_hash=True)
class Point:
    x: int
    y: int

    def __add__(self, other):
        return Point(x=self.x + other.x, y=self.y + other.y)

    def as_tuple(self):
        return self.x, self.y


@dataclass(frozen=True, unsafe_hash=True)
class Rock:
    points: tuple[Point]

    def create(self, rocks):
        hi = max(p.y for p in rocks) if rocks else -1
        return Rock(tuple(p + Point(2, hi + 4) for p in self.points))

    def move(self, to):
        if to == "v":
            move = Point(0, -1)  # y is 0 at floor. rocks go up
        elif to == ">":
            move = Point(1, 0)
        elif to == "<":
            move = Point(-1, 0)

        new = [p + move for p in self.points]
        if any(p.x < 0 or p.x > 6 for p in new):
            return self

        return Rock(tuple(new))


def read_input():
    with open("input") as f:
        return list(f.read().strip())


def draw(rocks):
    return
    time.sleep(0.5)
    os.system("clear")

    maxx = 6
    maxy = max(max(p.y for p in rocks), 7)
    for y in range(maxy, -1, -1):
        print("".join(("#" if Point(x, y) in rocks else ".") for x in range(maxx + 1)))


def simulate(paint=True):
    defrocks = itertools.cycle(
        [
            Rock((Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0))),
            Rock((Point(1, 0), Point(0, 1), Point(1, 1), Point(2, 1), Point(1, 2))),
            Rock((Point(0, 0), Point(1, 0), Point(2, 0), Point(2, 1), Point(2, 2))),
            Rock((Point(0, 0), Point(0, 1), Point(0, 2), Point(0, 3))),
            Rock((Point(0, 0), Point(0, 1), Point(1, 0), Point(1, 1))),
        ]
    )
    jets = itertools.cycle(read_input())
    rocks = set()

    while True:
        newrock = next(defrocks).create(rocks)
        if paint:
            draw(rocks | set(newrock.points))

        while True:
            move = next(jets)
            pushed = newrock.move(move)
            if not any(p in rocks for p in pushed.points):
                newrock = pushed

            if paint:
                draw(rocks | set(newrock.points))
            pushed = newrock.move("v")
            if any(p.y < 0 or p in rocks for p in pushed.points):
                break
            newrock = pushed
            if paint:
                draw(rocks | set(newrock.points))

        rocks.update(newrock.points)
        if paint:
            draw(rocks)

        yield max(p.y for p in rocks) + 1


def main():
    seq = []

    sim = simulate(paint=False)
    for it in trange(7500):
        height = next(sim)

        if it == 2021:
            print("Part 1:", height)

        # collect result after every full cycle of rock types
        if it and it % 5 == 0:
            seq.append(height)

    for idx in range(1, len(seq)):
        # skip the first 50 to wait for the pattern to stabilize
        diff = seq[50 + idx] - seq[50]
        if diff * 2 == seq[idx * 2 + 50] - seq[50] and diff * 3 == seq[idx * 3 + 50] - seq[50]:
            break
    else:
        raise RuntimeError("Cannot find pattern")

    target = 1000000000000 // 5  # samples are collected every 5 iterations
    closest = target - 50 - ((target - 50) % idx)  # closest iter that exactly matches the pattern
    assert closest % idx == 0
    pattern = closest // idx
    res = (pattern * diff) + seq[target - closest - 1] - 1
    print("Part 2:", res)


if __name__ == "__main__":
    main()
