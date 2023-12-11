# type: ignore

import re
import itertools
from collections import defaultdict


def read_input():
    valves = {}
    with open("input") as f:
        for line in f:
            if not line.strip():
                continue
            ptrn = r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.+)$"
            name, flow, tnls = re.search(ptrn, line).groups()
            valves[name] = (int(flow), tnls.split(", "))

    return valves


def allpaths(grid, valves):
    start = "AA"
    paths = {k: {j: 1 for j in grid[k][1]} for k in grid}

    def dist(a, b, seen=()):
        if b in paths[a]:
            return paths[a][b]
        exp = [c for c in grid[a][1] if c not in seen]
        if not exp:
            return float("inf")
        return min(dist(c, b, (*seen, a)) for c in exp) + 1

    for a, b in itertools.combinations([start, *valves], 2):
        c = dist(a, b)
        paths[a][b] = c
        paths[b][a] = c

    return paths


grid = read_input()
paths = allpaths(grid, {k for k in grid if grid[k][0]})


def mostpress(valves=None, maxt=30):
    start = "AA"
    if valves is None:
        valves = {k for k in grid if grid[k][0]}

    best = 0
    pending = [(0, 0, start, ())]
    while pending:
        time, pressure, node, opened = pending.pop()
        best = max(best, pressure)

        for other in valves:
            if other in opened:
                continue

            newtime = time + paths[node][other] + 1
            if newtime >= maxt:
                continue

            newpressure = pressure + (maxt - newtime) * grid[other][0]
            new = (newtime, newpressure, other, (*opened, other))
            pending.append(new)

    return best


def part1():
    return mostpress()


def part2():
    best = 0
    valves = {k for k in grid if grid[k][0]}
    splits = len(valves) // 2 + len(valves) % 2

    for you in itertools.combinations(valves, splits):
        elephant = valves - set(you)
        pressure = mostpress(you, 26) + mostpress(elephant, 26)
        best = max(best, pressure)

    return best


if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
