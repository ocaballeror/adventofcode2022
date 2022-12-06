# type: ignore

def marker(data, length):
    buffer = []
    for idx, char in enumerate(data):
        if char in buffer:
            got = buffer.index(char)
            buffer = buffer[got+1:]

        buffer.append(char)
        if len(buffer) == length:
            return idx + 1


if __name__ == "__main__":
    with open("input") as f:
        data = f.read().strip()

    print("Part 1:", marker(data, 4))
    print("Part 2:", marker(data, 14))
