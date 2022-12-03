def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


def value(let):
    if common.islower():
        return ord(let) - ord('a') + 1
    return ord(let) - ord('A') + 27


with open("input") as f:
    rucksacks = [line.strip() for line in f]

    total = 0
    for sack in rucksacks:
        assert len(sack) % 2 == 0
        common = set(sack[: len(sack) // 2]) & set(sack[len(sack) // 2:])
        assert len(common) == 1
        common = common.pop()
        total += value(common)

    print("Part 1:", total)

    total = 0
    for group in chunks(rucksacks, 3):
        common = set(group[0])
        combined = ""
        for elf in group:
            common &= set(elf)
            combined += elf
        assert len(common) == 1
        common = common.pop()
        total += value(common)

    print("Part 2:", total)
