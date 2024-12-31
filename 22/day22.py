# type: ignore

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

    def move(self, to):
        if to == 'R':
            return self + Point(1, 0)
        if to == 'L':
            return self + Point(-1, 0)
        if to == 'U':
            return self + Point(0, -1)
        if to == 'D':
            return self + Point(0, 1)

    def as_tuple(self):
        return self.x, self.y


def read_input():
    board = []
    with open("input") as f:
        for y, line in enumerate(f):
            line = line.strip('\n')
            if line:
                board.append(line)

    path = board.pop(-1)
    path = path.replace('L', ' L ').replace('R', ' R ').split()
    path = [int(thing) if thing.isnumeric() else thing for thing in path]

    return board, path

def firstlast(line):
    first = next(idx for idx, char in enumerate(line) if char != ' ')
    last = next(idx for idx, char in enumerate(reversed(line)) if char != ' ')
    last = len(line) - last

    return first, last


def part1():
    board, path = read_input()
    posx, _ = firstlast(board[0])
    pos = Point(posx, 0)
    breakpoint()
    look = 'R'
    for inst in path:
        if isinstance(inst, str):
            look = {
                'R': {'R': 'D', 'L': 'U'},
                'L': {'R': 'U', 'L': 'D'},
                'U': {'R': 'R', 'L': 'L'},
                'D': {'R': 'R', 'L': 'R'},
            }[look][inst]
            continue

        for _ in range(inst):
            # if pos.as_tuple() == (3, 7):
            #     breakpoint()
            newx, newy = pos.move(look).as_tuple()
            minx, maxx = firstlast(board[newy])
            miny, maxy = firstlast([row[newx] if newx < len(row) else ' ' for row in board])
            if not (minx <= newx <= maxx) or not (miny <= newy <= maxy):
                if look == 'R':
                    newx = minx
                if look == 'L':
                    newx = maxx
                if look == 'U':
                    newy = maxy
                if look == 'D':
                    newy = miny
            if board[newy][newx] == '.':
                pass
            elif board[newy][newx] == '#':
                break

            pos = Point(newx, newy)
            print(pos)

    return (pos.y + 1) * 1000 + (pos.x + 1) * 4 + 'RDLU'.index(look)


def part2():
    data = read_input()


if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
