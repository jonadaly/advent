from collections import defaultdict
from pathlib import Path

raw_input = Path("09.txt").read_text().strip()

# Hacked my way through this one - very messy and I don't think it's worth tidying up as it's not particularly elegant.
parsed_input: list[int | None] = []
parsed_input_2: dict[int, dict] = defaultdict(
    lambda: {"size": 0, "free_after": 0, "start_at_idx": 0}
)
current_id = 0
for i, c in enumerate(raw_input):
    if i % 2 == 0:
        start_idx = sum(p["size"] + p["free_after"] for p in parsed_input_2.values())
        parsed_input += [current_id] * int(c)
        parsed_input_2[current_id]["size"] = int(c)
        parsed_input_2[current_id]["start_at_idx"] = start_idx
    else:
        parsed_input += [None] * int(c)
        parsed_input_2[current_id]["free_after"] = int(c)
        current_id += 1

# Part 1
flipped = [c for c in parsed_input[::-1] if c is not None]
ptr_src = 0
output: list[int] = []
for page in parsed_input:
    if page is None:
        output.append(flipped[ptr_src])
        ptr_src += 1
    else:
        output.append(page)
    if len(output) >= len(flipped):
        break
checksum = sum(int(c) * i for i, c in enumerate(output))
print(f"Part 1: Checksum is {checksum}")


# Part 2
files = [{"_id": i, **v} for i, v in parsed_input_2.items()]


def do_part_2(_files: list[dict]) -> list[dict]:
    current_state = _files.copy()
    for file in _files[::-1]:
        file_with_space = None
        for idx, cand_file in enumerate(current_state):
            if cand_file["start_at_idx"] >= file["start_at_idx"]:
                break
            file_after = current_state[idx + 1]
            if (
                file_after["start_at_idx"]
                - cand_file["start_at_idx"]
                - cand_file["size"]
                >= file["size"]
            ):
                file_with_space = cand_file
                break
        if file_with_space is None:
            continue
        # Found match. Update state.
        new_state = current_state.copy()
        src_file = next(f for f in new_state if f["_id"] == file["_id"])
        dst_file = next(f for f in new_state if f["_id"] == file_with_space["_id"])
        src_file["start_at_idx"] = dst_file["start_at_idx"] + dst_file["size"]
        current_state = sorted(new_state, key=lambda x: x["start_at_idx"])
    return current_state


result1 = do_part_2(files)
back_to_raw = [result1[0]["_id"]] * result1[0]["size"]
for i in range(1, len(result1)):
    prev_file = result1[i - 1]
    curr_file = result1[i]
    back_to_raw += [None] * (
        curr_file["start_at_idx"] - prev_file["start_at_idx"] - prev_file["size"]
    )
    back_to_raw += [curr_file["_id"]] * curr_file["size"]

checksum_2 = sum(int(c) * i for i, c in enumerate(back_to_raw) if c)
print(f"Part 2: Checksum is {checksum_2}")
# 6488291456470
