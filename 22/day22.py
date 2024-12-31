# type: ignore

import re
from functools import cached_property
from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int

    def __add__(self, other):
        return Point(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def valid(self, board):
        try:
            return board[self.y][self.x] != ' '
        except IndexError:
            return False

    def move(self, to, board):
        if to == ">":
            return Point(self.x + 1, self.y)

        elif to == "<":
            return Point(self.x - 1, self.y)

        elif to == "^":
            return Point(self.x, self.y - 1)

        elif to == "v":
            return Point(self.x, self.y + 1)

    def wrap(self, face, board):
        minx, maxx = firstlast(board[self.y])
        miny, maxy = firstlast([row[self.x] for row in board])

        if face == '>':
            return Point(minx, self.y), face
        elif face == '<':
            return Point(maxx, self.y), face
        elif face == 'v':
            return Point(self.x, miny), face
        elif face == '^':
            return Point(self.x, maxy), face

    def bend(self, face, board):
        transform = {
            (2, ">"): lambda p: (Point(maxx(4), maxy(4) - (p.y - miny(2))), "<"),
            (3, ">"): lambda p: (Point(minx(2) + (p.y - miny(3)), maxy(2)), "^"),
            (4, ">"): lambda p: (Point(maxx(2), maxy(2) - (p.y - miny(4))), "<"),
            (6, ">"): lambda p: (Point(minx(4) + (p.y - miny(6)), maxy(4)), "^"),
            (2, "v"): lambda p: (Point(maxx(3), miny(3) + (p.x - minx(2))), "<"),
            (4, "v"): lambda p: (Point(maxx(6), miny(6) + (p.x - minx(4))), "<"),
            (6, "v"): lambda p: (Point(minx(2) + (p.x - minx(6)), 0), "v"),
            (1, "<"): lambda p: (Point(minx(5), maxy(5) - (p.y - miny(1))), ">"),
            (3, "<"): lambda p: (Point(minx(5) + (p.y - miny(3)), miny(5)), "v"),
            (5, "<"): lambda p: (Point(minx(1), maxy(1) - (p.y - miny(5))), ">"),
            (6, "<"): lambda p: (Point(minx(1) + (p.y - miny(6)), miny(1)), "v"),
            (1, "^"): lambda p: (Point(minx(6), miny(6) + (p.x - minx(1))), ">"),
            (2, "^"): lambda p: (Point(minx(6) + (p.x - minx(2)), maxy(6)), "^"),
            (5, "^"): lambda p: (Point(minx(3), miny(3) + (p.x - minx(5))), ">"),
        }
        return transform[self.cube(), face](self)

    def cube(self):
        for num in range(1, 7):
            if minx(num) <= self.x <= maxx(num) and miny(num) <= self.y <= maxy(num):
                return num


def minx(n):
    return {1: 50, 2: 100, 3: 50, 4: 50, 5: 0, 6: 0}[n]


def maxx(n):
    return {1: 99, 2: 149, 3: 99, 4: 99, 5: 49, 6: 49}[n]


def miny(n):
    return {1: 0, 2: 0, 3: 50, 4: 100, 5: 100, 6: 150}[n]


def maxy(n):
    return {1: 49, 2: 49, 3: 99, 4: 149, 5: 149, 6: 199}[n]


def read_input():
    board = []
    with open("input") as f:
        for y, line in enumerate(f):
            line = line.removesuffix("\n")
            if line:
                board.append(line)

    path = board.pop(-1)
    path = path.replace("L", " < ").replace("R", " > ").split()
    path = [int(thing) if thing.isnumeric() else thing for thing in path]

    maxx = max(len(line) for line in board)
    board = [line + " " * (maxx - len(line)) for line in board]

    return board, path


def firstlast(line):
    first = next(idx for idx, char in enumerate(line) if char != " ")
    last = next(idx for idx, char in enumerate(reversed(line)) if char != " ")
    last = len(line) - last - 1

    return first, last


def simulate(teleport):
    board, path = read_input()
    posx, _ = firstlast(board[0])
    pos = Point(posx, 0)
    look = ">"
    for inst in path:
        if isinstance(inst, str):
            turns = '>v<^'
            look = turns[(turns.index(look) + (1 if inst == '>' else -1)) % 4]
            continue

        for _ in range(inst):
            newlook = look
            new = pos.move(look, board)

            if not new.valid(board):
                new, newlook = getattr(pos, teleport)(look, board)
                assert new.valid(board)

            if board[new.y][new.x] == '#':
                break

            assert board[pos.y][pos.x] == "."
            pos = new
            look = newlook

    return (pos.y + 1) * 1000 + (pos.x + 1) * 4 + ">v<^".index(look)


def part1():
    return simulate('wrap')


def part2():
    return simulate('bend')


if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
