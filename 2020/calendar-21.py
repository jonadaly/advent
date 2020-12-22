from pathlib import Path
from typing import List, Tuple, Dict, Set
import re

raw_foods = Path("21.txt").read_text().strip().split("\n")

foods: List[Dict] = []
for food in raw_foods:
    groups = re.match(r"^(.+) \(contains (.+)\)$", food).groups()
    foods.append(
        {
            "ingredients": set(groups[0].split(" ")),
            "allergens": set(groups[1].split(", ")),
        }
    )
all_allergens: Set[str] = set().union(*[f["allergens"] for f in foods])
all_ingredients: Set[str] = set().union(*[f["ingredients"] for f in foods])

allergen_map: Dict[str, str] = {}
while len(allergen_map) < len(all_allergens):
    for allergen in all_allergens:
        possible_ingredients = all_ingredients.copy()
        for food in foods:
            if allergen in food["allergens"]:
                possible_ingredients &= food["ingredients"]
        possible_ingredients -= set(
            allergen_map.values()
        )
        if len(possible_ingredients) == 1:
            allergen_map[allergen] = list(possible_ingredients)[0]
            continue
# print(f"Allergens: {allergen_map}")

safe_ingredients = all_ingredients - set(allergen_map.values())
safe_ingredient_appearances = sum(
    1 for f in foods for i in f["ingredients"] if i in safe_ingredients
)
print(f"Part 1: Safe ingredients appear {safe_ingredient_appearances} times")

dangerous_ingredients = [allergen_map[a] for a in sorted(list(allergen_map.keys()))]
print("Part 2: Dangerous ingredients: " + ",".join(dangerous_ingredients))
