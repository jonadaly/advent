import re

with open("24.txt", "r") as f:
    inputs = f.read()

# inputs = """Immune System:
# 17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
# 989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

# Infection:
# 801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
# 4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4"""


class Group:
    def __init__(
        self,
        idx,
        team,
        units,
        hp,
        damage,
        damage_type,
        immunities,
        weaknesses,
        initiative,
    ):
        self.idx = idx
        self.team = team
        self.units = units
        self.hp = hp
        self.damage = damage
        self.damage_type = damage_type
        self.immunities = immunities
        self.weaknesses = weaknesses
        self.initiative = initiative
        self.target = None
        self.targeted = False

    def __repr__(self):
        return f"{self.team} group {self.idx}: {self.units} units @ {self.hp} HP, {self.damage} {self.damage_type} damage (int {self.initiative}, pow {self.power})"

    @property
    def power(self):
        return self.units * self.damage


def parse_group(line, team, idx, boost):
    match = regex.search(line)
    units = int(match.group(1))
    hp = int(match.group(2))
    buffs = match.group(3)
    damage = int(match.group(4)) + boost
    damage_type = match.group(5)
    initiative = int(match.group(6))
    immunities = []
    weaknesses = []
    if buffs is not None:
        for buff in buffs[1:-2].split(";"):
            if buff.strip().startswith("immune"):
                immunities = [i.strip() for i in buff[10:].split(",")]
            elif buff.strip().startswith("weak"):
                weaknesses = [w.strip() for w in buff[8:].split(",")]
            else:
                raise ValueError(f"Unexpected buff wording: {buff}")
    return Group(
        idx, team, units, hp, damage, damage_type, immunities, weaknesses, initiative
    )


def select_targets(groups):
    # print("TARGET!!!")
    groups = sorted(groups, key=lambda x: (x.power, x.initiative), reverse=True)
    for group in groups:
        group.targeted = False
        group.target = None
    for group in groups:
        if group.units <= 0:
            # print(f"Group: {group}\nDead")
            continue
        best_total_damage = 0
        best_target = None
        for cand in [
            g
            for g in groups
            if g.team != group.team and g.targeted is False and g.units > 0
        ]:
            if group.damage_type in cand.weaknesses:
                total_damage = 2 * group.power
            elif group.damage_type in cand.immunities:
                total_damage = 0
            else:
                total_damage = group.power
            if total_damage == 0:
                continue
            if total_damage > best_total_damage or best_target is None:
                best_total_damage = total_damage
                best_target = cand
            if total_damage == best_total_damage and cand.power > best_target.power:
                best_total_damage = total_damage
                best_target = cand
            if (
                total_damage == best_total_damage
                and cand.power == best_target.power
                and cand.initiative > best_target.initiative
            ):
                best_total_damage = total_damage
                best_target = cand
        if best_target is None:
            # print(f"Group: {group}\nNo Target")
            continue
        group.target = best_target
        best_target.targeted = True
        # print(f"Group: {group}\nTarget: {group.target} (damage: {best_total_damage})\n")


def perform_attacks(groups):
    # print("ATTACK!!!")
    groups = sorted(groups, key=lambda x: x.initiative, reverse=True)
    for group in groups:
        if group.units <= 0 or group.target is None:
            continue
        if group.damage_type in group.target.weaknesses:
            total_damage = 2 * group.power
        elif group.damage_type in group.target.immunities:
            total_damage = 0
        else:
            total_damage = group.power
        unit_reduction = total_damage // group.target.hp
        group.target.units -= unit_reduction
        # print(f"Group: {group}\nTarget: {group.target} (units lost: {unit_reduction})\n")


def do_the_thing(boost):
    groups = []
    for i, line in enumerate(inputs.split("\n\n")[0].strip().split("\n")[1:]):
        groups.append(parse_group(line, "immune", i + 1, boost))
    for i, line in enumerate(inputs.split("\n\n")[1].strip().split("\n")[1:]):
        groups.append(parse_group(line, "infection", i + 1, 0))

    groups = sorted(groups, key=lambda x: (x.power, x.initiative), reverse=True)
    # for group in groups:
    #     print(group)
    #     print(f"Weaknesses: {group.weaknesses}")
    #     print(f"Immunities: {group.immunities}")
    # print("\n")

    round_idx = 1
    while True:
        # print(f"round {round_idx}")
        select_targets(groups)
        if not any(g for g in groups if g.target is not None):
            winning_units = sum([g.units for g in groups if g.units > 0])
            winning_team = next(g.team for g in groups if g.units > 0)
            return winning_units, winning_team
        perform_attacks(groups)
        if round_idx > 10000:
            print("Skipping")
            return -1, "stalemate"
        round_idx += 1


regex = re.compile(
    r"(\d+) units each with (\d+) hit points (\([^)]+\) )?with an attack that does (\d+) (\w+) damage at initiative (\d+)"
)

# Part 1
winning_units, winning_team = do_the_thing(0)
print(f"Part 1: {winning_units} units left in winning {winning_team} army")

# Part 2
boost = 0
while True:
    winning_units, winning_team = do_the_thing(boost)
    print(
        f"Part 2: {winning_units} units left in winning {winning_team} army - boost {boost}"
    )
    if winning_team == "immune":
        break
    boost += 1
