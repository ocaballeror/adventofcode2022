import heapq


class Grid:
    def __init__(self, data):
        self.grid = data

    def __getitem__(self, acc):
        x, y = acc
        return self.grid[y][x]

    def __contains__(self, acc):
        x, y = acc
        return 0 <= x < self.cols and 0 <= y < self.rows

    @property
    def rows(self):
        return len(self.grid)

    @property
    def cols(self):
        return len(self.grid[0])

    def adjacent(self, point):
        x, y = point
        for movex, movey in [
            (-1, 0),
            (0, -1),
            (0, 1),
            (1, 0),
        ]:
            move = x + movex, y + movey
            if move in self and self[move] - self[point] < 2:
                yield x + movex, y + movey

    def draw(self):
        for y in range(self.rows):
            print("".join(chr(self[(x, y)] + 97) for x in range(self.cols)))
        print("")


def dijkstra(grid, start, end):
    # grid.draw()
    seen = set()
    pending = [(0, start)]
    pset = set(pending)  # set copy of `pending` for faster membership checks
    while pending:
        cost, node = heapq.heappop(pending)
        pset.remove((cost, node))
        if node == end:
            return cost

        for move in grid.adjacent(node):
            if move in seen:
                continue
            new = (cost + 1, move)
            if new in pset:
                continue
            heapq.heappush(pending, new)
            pset.add(new)

        seen.add(node)

    return -1


def read_input():
    with open("input") as f:
        grid = []
        start = (0, 0)
        end = (0, 0)
        for y, line in enumerate(f):
            row = []
            for x, val in enumerate(line.strip()):
                if val == "S":
                    row.append(0)
                    start = (x, y)
                elif val == "E":
                    row.append(25)
                    end = (x, y)
                else:
                    row.append(ord(val) - 97)

            grid.append(row)

        return Grid(grid), start, end


def part1():
    return dijkstra(*read_input())


def part2():
    grid, _, end = read_input()

    lows = [(x, y) for x in range(grid.cols) for y in range(grid.rows) if grid[x, y] == 0]

    return min(dist for start in lows if (dist := dijkstra(grid, start, end)) != -1)


if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
