from pathlib import Path

raw_input = Path("12.txt").read_text().strip().split("\n")
farm: dict[complex, str] = {
    i + ii * 1j: char
    for i, line in enumerate(raw_input)
    for ii, char in enumerate(line)
}

# Find all regions (will contain duplicates)
all_regions = {f: {f} for f in farm}
for coord in all_regions:
    for dir in coord + 1, coord + 1j, coord - 1, coord - 1j:
        if farm.get(dir) == farm[coord]:
            all_regions[coord] |= all_regions[dir]
            for r in all_regions[coord]:
                all_regions[r] = all_regions[coord]

# Find unique regions as a set of sets (frozenset is to make it hashable)
regions: set[frozenset[complex]] = {frozenset(r) for r in all_regions.values()}


def area(region: frozenset[complex]) -> int:
    return len(region)


def perimeter(region: frozenset[complex]) -> int:
    # Each cell adds 4 units to the perimeter, minus 1 for any adjacent cell in the region.
    perimeter = 0
    for r in region:
        for dir in r + 1, r + 1j, r - 1, r - 1j:
            if dir not in region:
                perimeter += 1
    return perimeter


def sides(region: frozenset[complex]) -> int:
    # Number of sides is the same as the number of corners.
    sides = 0
    for r in region:
        for dir in (1, 1), (1, -1), (-1, 1), (-1, -1):
            if (
                r + complex(0, dir[1]) not in region
                and r + complex(dir[0], 0) not in region
            ):
                # External corner, because this pair of orthogonal sides are both not in the region.
                sides += 1
            elif (
                r + complex(0, dir[1]) in region
                and r + complex(dir[0], 0) in region
                and r + complex(dir[0], dir[1]) not in region
            ):
                # Internal corner, because this pair of orthogonal sides are both in the region, but the diagonal is not.
                sides += 1
    return sides


price_p1 = sum(area(r) * perimeter(r) for r in regions)
print(f"Part 1: price is {price_p1}")
price_p2 = sum(area(r) * sides(r) for r in regions)
print(f"Part 2: price is {price_p2}")
