most = []
with open("input") as f:
    count = 0
    for line in f:
        line = line.strip()
        if not line:
            if len(most) < 3:
                most.append(count)
            elif count > most[0]:
                most.append(count)
                most.sort()
                most = most[1:]
            count = 0
        else:
            count += int(line)


print("Part 1:", most[-1])
print("Part 2:", sum(most))
