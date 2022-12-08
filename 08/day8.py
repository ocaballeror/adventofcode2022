# type: ignore
from collections import defaultdict

with open("input") as f:
    grid = [[int(c) for c in line.strip()] for line in f]


def part1():
    visible = set()

    for y, row in enumerate(grid):
        # left to right
        hi = -1
        for x, tree in enumerate(row):
            if tree > hi:
                hi = tree
                print(f"Add {tree=} at {(x, y)}")
                visible.add((x, y))

        # right to left
        hi = -1
        for x, tree in enumerate(reversed(row)):
            if tree > hi:
                hi = tree
                x = len(row) - x - 1
                print(f"Add {tree=} at {(x, y)}")
                visible.add((x, y))

    for x in range(len(grid[0])):
        col = [row[x] for row in grid]

        # up down
        hi = -1
        for y, tree in enumerate(col):
            if tree > hi:
                hi = tree
                print(f"Add {tree=} at {(x, y)}")
                visible.add((x, y))

        # down up
        hi = -1
        for y, tree in enumerate(reversed(col)):
            if tree > hi:
                hi = tree
                y = len(col) - y - 1
                print(f"Add {tree=} at {(x, y)}")
                visible.add((x, y))

    return len(visible)


def score(line):
    def _score(row):
        acc = []
        for idx, val in enumerate(row):
            count = 0
            for other in reversed(row[:idx]):
                count += 1
                if other >= val:
                    break
            acc.append(count)

        return acc

    return [a * b for a, b in zip(_score(line), reversed(_score(line[::-1])))]


def part2():
    vals = defaultdict(lambda: 1)

    for y, row in enumerate(grid):
        for x, tree in enumerate(score(row)):
            vals[(x, y)] *= tree

    for x in range(len(grid[0])):
        col = [row[x] for row in grid]

        for y, tree in enumerate(score(col)):
            vals[(x, y)] *= tree

    return max(vals.values())


if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
