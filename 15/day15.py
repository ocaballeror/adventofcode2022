import re
from functools import cached_property
from dataclasses import dataclass


@dataclass(unsafe_hash=True, frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other):
        return Point(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def as_tuple(self):
        return self.x, self.y


@dataclass(frozen=True)
class Sensor(Point):
    beacon: Point = None

    @cached_property
    def dist(self):
        return self - self.beacon


def parse_input():
    sensors = []
    with open("input") as f:
        for line in f:
            (sensx, sensy), (beacx, beacy) = re.findall(
                r'x=(-?\d+), y=(-?\d+)', line
            )
            sensors.append(
                Sensor(
                    x=int(sensx),
                    y=int(sensy),
                    beacon=Point(int(beacx), int(beacy)),
                )
            )

    return sensors


def part1():
    # line = 10
    line = 2000000
    sensors = parse_input()
    beacons = set()

    covered = set()
    for sens in sensors:
        if sens.beacon.y == line:
            beacons.add(sens.beacon.x)
        lgth = sens.dist - abs(sens.y - line)
        if lgth < 0:
            continue
        for x in range(sens.x - lgth, sens.x + lgth + 1):
            covered.add(x)

    covered -= beacons
    return len(covered)


def part2():
    # limit = 20
    limit = 4000000
    sensors = parse_input()
    for sens in sensors:
        for y in range(sens.dist + 1):
            for move in [
                (sens.dist - y + 1, y),
                (y - sens.dist - 1, y),
                (y, sens.dist - y + 1),
                (y, y - sens.dist - 1),
            ]:
                edge = sens + Point(*move)
                if edge.x < 0 or edge.y < 0 or edge.x > limit or edge.y > limit:
                    continue
                if not any(s for s in sensors if edge - s <= s.dist):
                    return edge.x * 4000000 + edge.y


if __name__ == '__main__':
    print("Part 1:", part1())
    print("Part 2:", part2())
