from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int

    def __add__(self, other):
        return Point(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other):
        return Point(x=self.x - other.x, y=self.y - other.y)

    def as_tuple(self):
        return self.x, self.y


with open("input") as f:
    moves = [(inst[0], int(inst[1])) for line in f if (inst := line.strip().split())]


def sim(ropelen=2):
    head = Point(0, 0)
    rope = [Point(0, 0) for _ in range(ropelen-1)]
    seen = {(0, 0)}

    for to, count in moves:
        for _ in range(count):
            if to == 'U':
                head.y -= 1
            elif to == 'D':
                head.y += 1
            elif to == 'R':
                head.x += 1
            elif to == 'L':
                head.x -= 1

            last = head
            for point in rope:
                dist = last - point
                if abs(dist.x) + abs(dist.y) > 2:
                    point.x += dist.x // abs(dist.x)
                    point.y += dist.y // abs(dist.y)
                elif abs(dist.x) == 2:
                    point.x += dist.x // abs(dist.x)
                elif abs(dist.y) == 2:
                    point.y += dist.y // abs(dist.y)

                last = point

            seen.add(rope[-1].as_tuple())

    return len(seen)


print("Part 1:", sim(2))
print("Part 2:", sim(10))
