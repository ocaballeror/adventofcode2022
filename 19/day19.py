import re
import multiprocessing
from dataclasses import dataclass, field
from collections import defaultdict
from functools import cached_property, cache


def read_input():
    blueprints = []
    with open("input") as f:
        for line in f:
            nums = list(map(int, re.findall(r"\d+", line)))
            assert len(nums) == 7
            blueprints.append((nums[1], nums[2], (nums[3], nums[4]), (nums[5], nums[6])))

    return blueprints


@dataclass(repr=True, kw_only=True, frozen=True)
class State:
    minutes: int = 24
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geodes: int = 0
    orerobots: int = 1
    clayrobots: int = 0
    obsidianrobots: int = 0
    geoderobots: int = 0
    orecost: int = field(default=0, repr=False, compare=False)
    claycost: int = field(default=0, repr=False, compare=False)
    obsidiancost: tuple[int, int] = field(default=(0, 0), repr=False, compare=False)
    geodecost: tuple[int, int] = field(default=(0, 0), repr=False, compare=False)
    bought: str | None = None

    @classmethod
    def from_blueprint(cls, blueprint):
        orecost, claycost, obsidiancost, geodecost = blueprint
        return cls(
            orecost=orecost, claycost=claycost, obsidiancost=obsidiancost, geodecost=geodecost
        )

    @property
    def blueprint(self):
        return self.orecost, self.claycost, self.obsidiancost, self.geodecost

    def collect(self):
        return self.replace(
            ore=min(
                self.ore + self.orerobots,
                max(self.orecost, self.claycost, self.obsidiancost[0], self.geodecost[0]) * 2,
            ),
            clay=min(self.clay + self.clayrobots, self.obsidiancost[1] * 2),
            obsidian=min(self.obsidian + self.obsidianrobots, self.geodecost[1] * 2),
            geodes=self.geodes + self.geoderobots,
            minutes=self.minutes - 1,
        )

    def dict(self):
        return {k: getattr(self, k) for k in self.__annotations__}

    def replace(self, **kwargs):
        return State(**(self.dict() | kwargs))

    def canbuy(self, kind):
        match kind:
            case "geode":
                return self.ore >= self.geodecost[0] and self.obsidian >= self.geodecost[1]
            case "ore":
                return self.ore >= self.orecost
            case "clay":
                return self.ore >= self.claycost
            case "obsidian":
                return self.ore >= self.obsidiancost[0] and self.clay >= self.obsidiancost[1]

    @property
    def prev(self):
        return self.replace(
            ore=self.ore - self.orerobots - (1 if self.bought == 'ore' else 0),
            clay=self.clay - self.clayrobots - (1 if self.bought == 'clay' else 0),
            obsidian=self.obsidian - self.obsidianrobots - (1 if self.bought == 'obsidian' else 0),
            geodes=self.geodes - self.geoderobots - (1 if self.bought == 'geodes' else 0),
        )


    def shouldbuy(self, kind):
        return self.canbuy(kind) and (self.bought or not self.prev.canbuy(kind))

    def buy(self, kind):
        if not self.shouldbuy(kind):
            return

        new = self.collect()
        match kind:
            case "geode":
                new = new.replace(
                    ore=new.ore - self.geodecost[0],
                    obsidian=new.obsidian - self.geodecost[1],
                    geoderobots=self.geoderobots + 1,
                    bought=kind,
                )
            case "ore":
                new = new.replace(
                    ore=new.ore - self.orecost,
                    orerobots=self.orerobots + 1,
                    bought=kind,
                )
            case "clay":
                new = new.replace(
                    ore=new.ore - self.claycost,
                    clayrobots=self.clayrobots + 1,
                    bought=kind,
                )
            case "obsidian":
                new = new.replace(
                    ore=new.ore - self.obsidiancost[0],
                    clay=new.clay - self.obsidiancost[1],
                    obsidianrobots=self.obsidianrobots + 1,
                    bought=kind,
                )

        return new

    @cached_property
    def params(self):
        return (
            self.minutes,
            self.ore,
            self.clay,
            self.obsidian,
            self.orerobots,
            self.clayrobots,
            self.obsidianrobots,
            self.geodecost,
            self.obsidiancost,
            self.claycost,
            self.orecost,
        )


memo = {}
best = defaultdict(int)

@cache
def wish(minutes, base):
    """
    best case scenario for how many geodes we can get with n minutes left, assuming we create a
    new robot each minute
    """
    if minutes == 0:
        return 0
    return minutes - 1 + base + wish(minutes-1, base)


def optimize(state):
    if not state or state.minutes == 0:
        return state
    if state.params in memo:
        return memo[state.params]

    if state.blueprint in best and wish(state.minutes, state.geoderobots) + state.geodes < best[state.blueprint]:
        return state

    # if we can build geode or obsidian robots do that and ignore everything else
    if with_geode := state.buy("geode"):
        paths = [with_geode]
    elif with_obs := state.buy("obsidian"):
        paths = [with_obs]
    else:
        paths = [
            state.collect(),
            state.buy("clay"),
            state.buy("ore"),
        ]

    if not any(paths):
        return None

    res = max(map(optimize, paths), key=lambda x: x.geodes if x else -1)
    assert state.params not in memo
    if res and res.minutes == 0:
        best[state.blueprint] = max(best[state.blueprint], res.geodes)
    memo[state.params] = res
    return res


def part1():
    blueprints = read_input()
    acc = 0
    with multiprocessing.Pool() as pool:
        for idx, state in enumerate(pool.imap(optimize, map(State.from_blueprint, blueprints)), 1):
            print(idx, state.geodes)
            acc += idx * state.geodes

    return acc


def part2():
    blueprints = read_input()
    acc = 1
    with multiprocessing.Pool() as pool:
        states = [State.from_blueprint(bp).replace(minutes=32) for bp in blueprints[:3]]
        for idx, state in enumerate(pool.imap(optimize, states), 1):
            print(idx, state.geodes)
            acc *= state.geodes

    return acc


if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
