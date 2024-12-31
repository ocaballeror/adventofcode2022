# type: ignore
import itertools


def read_input():
    with open("input") as f:
        return [tuple(map(int, line.split(","))) for line in f if line.strip()]


def things(cubes):
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
    return things(read_input())

def part2():
    cubes = read_input()

    maxx = max(c[0] for c in cubes)
    maxy = max(c[1] for c in cubes)
    maxz = max(c[2] for c in cubes)

    left = lambda cube: (
        other
        for other in cubes
        if other[0] < cube[0] and other[1] == cube[1] and other[2] == cube[2]
    )
    right = lambda cube: (
        other
        for other in cubes
        if other[0] > cube[0] and other[1] == cube[1] and other[2] == cube[2]
    )
    above = lambda cube: (
        other
        for other in cubes
        if other[0] == cube[0] and other[1] < cube[1] and other[2] == cube[2]
    )
    below = lambda cube: (
        other
        for other in cubes
        if other[0] == cube[0] and other[1] > cube[1] and other[2] == cube[2]
    )
    front = lambda cube: (
        other
        for other in cubes
        if other[0] == cube[0] and other[1] == cube[1] and other[2] < cube[2]
    )
    behind = lambda cube: (
        other
        for other in cubes
        if other[0] == cube[0] and other[1] == cube[1] and other[2] > cube[2]
    )

    inside = 0
    for cube in cubes:
        cubex, cubey, cubez = cube

        other = next(right(cube), None)
        if (
            other
            and other[0] - cubex > 1
            and all(
                any(above((x, cubey, cubez)))
                and any(below((x, cubey, cubez)))
                and any(front((x, cubey, cubez)))
                and any(behind((x, cubey, cubez)))
                for x in range(cubex + 1, other[0])
            )
        ):
            sfc = sum(
                len(list(above((x, cubey, cubez))))
                + len(list((below((x, cubey, cubez)))))
                + len(list((front((x, cubey, cubez)))))
                + len(list((behind((x, cubey, cubez)))))
                for x in range(cubex + 1, other[0])
            )
            inside += sfc - 1
            print("procket", sfc, cube, other)

    a = things(cubes)
    return a - inside


if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
