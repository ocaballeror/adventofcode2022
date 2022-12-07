# type: ignore
from functools import cached_property
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class File:
    path: Path
    size: int


@dataclass
class Dir:
    path: Path
    files: list[File] = field(repr=False, default_factory=list)
    dirs: list["Dir"] = field(repr=False, default_factory=list)

    @cached_property
    def size(self):
        return sum(item.size for item in (*self.files, *self.dirs))


with open("input") as f:
    lines = [line.strip() for line in f]


root = Path('/')
fs = {root: Dir(root)}
cwd = root
for line in lines[1:]:
    if line.startswith('$'):
        parts = line.split()
        cmd = parts[1]
        if cmd != 'cd':
            continue
        arg = parts[2]
        if arg == '..':
            cwd = cwd.parent
        else:
            cwd /= arg
    else:
        size, fname = line.split()
        path = cwd / fname
        if size == 'dir':
            file = Dir(path)
            fs[cwd].dirs.append(file)
        else:
            file = File(path, int(size))
            fs[cwd].files.append(file)

        fs[path] = file


print("Part 1:", sum(f.size for f in fs.values() if isinstance(f, Dir) and f.size <= 100000))

total = 7e7
need = 3e7
have = total - fs[root].size
for thing in sorted((f for f in fs.values() if isinstance(f, Dir)), key=lambda x: x.size):
    if have + thing.size >= need:
        print("Part 2:", thing.size)
        break
