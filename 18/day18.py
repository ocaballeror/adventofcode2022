# type: ignore
import operator


def read_input():
    with open("input") as f:
        return [tuple(map(int, line.split(","))) for line in f if line.strip()]


def surface(cubes):
    cubes = set(cubes)

    coll = 0
    for cube in cubes:
        cubex, cubey, cubez = cube
        for movex, movey, movez in [
            (1, 0, 0),
            (-1, 0, 0),
            (0, 1, 0),
            (0, -1, 0),
            (0, 0, 1),
            (0, 0, -1),
        ]:
            if (cubex + movex, cubey + movey, cubez + movez) in cubes:
                coll += 1

    return len(cubes) * 6 - coll


def part1():
    return surface(read_input())


def between(one, other):
    onex, oney, onez = one
    otherx, othery, otherz = other

    for x in range(min(onex, otherx) + 1, max(onex, otherx)):
        assert oney == othery and onez == otherz
        yield x, oney, onez

    for y in range(min(oney, othery) + 1, max(oney, othery)):
        assert onex == otherx and onez == otherz
        yield onex, y, onez

    for z in range(min(onez, otherz) + 1, max(onez, otherz)):
        assert oney == othery and onex == otherx
        yield onex, oney, z


def part2():
    cubes = read_input()

    cubes_by_x = sorted(cubes, key=operator.itemgetter(0))
    cubes_by_y = sorted(cubes, key=operator.itemgetter(1))
    cubes_by_z = sorted(cubes, key=operator.itemgetter(2))

    left = lambda cube: (
        other
        for other in reversed(cubes_by_x)
        if other[0] < cube[0] and other[1] == cube[1] and other[2] == cube[2]
    )
    right = lambda cube: (
        other
        for other in cubes_by_x
        if other[0] > cube[0] and other[1] == cube[1] and other[2] == cube[2]
    )
    above = lambda cube: (
        other
        for other in reversed(cubes_by_y)
        if other[0] == cube[0] and other[1] < cube[1] and other[2] == cube[2]
    )
    below = lambda cube: (
        other
        for other in cubes_by_y
        if other[0] == cube[0] and other[1] > cube[1] and other[2] == cube[2]
    )
    front = lambda cube: (
        other
        for other in reversed(cubes_by_z)
        if other[0] == cube[0] and other[1] == cube[1] and other[2] < cube[2]
    )
    behind = lambda cube: (
        other
        for other in cubes_by_z
        if other[0] == cube[0] and other[1] == cube[1] and other[2] > cube[2]
    )

    seen = set()
    for cube in cubes:
        cubex, cubey, cubez = cube

        other = next(right(cube), None)
        if other and other[0] - cubex > 1:
            trap = [
                (
                    next(above(mid), None),
                    next(below(mid), None),
                    next(front(mid), None),
                    next(behind(mid), None),
                )
                for mid in between(cube, other)
            ]
            if all(b for a in trap for b in a):
                for mid, directions in zip(between(cube, other), trap):
                    seen.add(mid)
                    for wall in directions:
                        for third in between(mid, wall):
                            seen.add(third)

    return surface(cubes) - surface(seen)


if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
