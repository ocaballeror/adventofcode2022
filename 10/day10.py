# type: ignore
with open("input") as f:
    program = [tuple(line.strip().split()) for line in f]


cycle = 0
reg = 1
rem = 0
strength = 0
out = []
for inst in program:
    if inst[0] == "addx":
        rem = 2
        op = lambda r: r + int(inst[1])
    elif inst[0] == "noop":
        rem = 1
        op = lambda r: r

    while rem > 0:
        px = cycle % 40
        if reg in (px - 1, px, px + 1):
            out.append("#")
        else:
            out.append(".")

        rem -= 1
        cycle += 1
        if (cycle - 20) % 40 == 0:
            strength += cycle * reg
            # print(f"{cycle=} {reg=} strength={cycle * reg} {strength=}")

        if cycle % 40 == 0:
            out.append("\n")

    reg = op(reg)


print("Part 1:", strength)
print("".join(out), end="")
