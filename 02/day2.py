from collections import defaultdict

count = defaultdict(int)
with open("input") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        count[line[0]] += 1
        count[line[0]+line[2]] += 1
        count[line[2]] += 1

score = count['X'] + count['Y'] * 2 + count['Z'] * 3
score += (count['AX'] + count['BY'] + count['CZ']) * 3
score += (count['AY'] + count['BZ'] + count['CX']) * 6
print(count)
print("Part 1", score)

score = count['Y'] * 3 + count['Z'] * 6
score += (count['AY'] + count['BX'] + count['CZ']) * 1
score += (count['AZ'] + count['BY'] + count['CX']) * 2
score += (count['AX'] + count['BZ'] + count['CY']) * 3
print("Part 2", score)
