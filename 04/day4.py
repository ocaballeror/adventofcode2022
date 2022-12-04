with open("input") as f:
    contained = 0
    overlap = 0
    for line in f:
        line = line.strip()
        first, second = line.split(',')

        a, b = map(int, first.split('-'))
        c, d = map(int, second.split('-'))
        first = range(a, b + 1)
        second = range(c, d + 1)

        if (a <= c and b >= d) or (c <= a and d >= b):
            contained += 1
        if a in second or b in second or c in first or d in first:
            overlap += 1

    print("Part 1:", contained)
    print("Part 2:", overlap)
