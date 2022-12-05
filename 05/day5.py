# type: ignore

with open("input") as f:
    crates = []
    instructions = []
    gotcrates = False
    for line in f:
        if not line.strip():
            continue

        if not gotcrates:
            stacks = len(line) // 4
            linecrates = line[1::4]
            if linecrates[0] == '1':
                gotcrates = True
                crates = [
                    [a[i] for a in reversed(crates) if a[i] != ' '] for i in range(len(crates[0]))
                ]
            else:
                crates.append(linecrates)
        else:
            instructions.append([int(a) for a in line.split() if a.isnumeric()])


orig = [stack.copy() for stack in crates]
for amount, src, dest in instructions:
    for _ in range(amount):
        crates[dest-1].append(crates[src-1].pop())

print("Part 1:", ''.join(crt[-1] for crt in crates))

crates = orig
for amount, src, dest in instructions:
    crates[dest-1].extend(crates[src-1][-amount:])
    crates[src-1] = crates[src-1][:-amount]

print("Part 2:", ''.join(crt[-1] for crt in crates))
