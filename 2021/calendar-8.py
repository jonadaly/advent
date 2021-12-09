from pathlib import Path

displays_raw = Path("8.txt").read_text().strip().split("\n")

displays: dict = {}
for i, display_raw in enumerate(displays_raw):
    parts = display_raw.split("|")
    displays[i] = {
        "possibilities": parts[0].strip().split(),
        "raw_displays":parts[1].strip().split(),
        "decoded_displays": [None, None, None, None]
    }

count = 0
for i_display, display in displays.items():
    segments_in_one = set(next(p for p in display["possibilities"] if len(p) == 2))
    segments_in_four = set(next(p for p in display["possibilities"] if len(p) == 4))
    segments_in_seven = set(next(p for p in display["possibilities"] if len(p) == 3))
    segments_in_four_but_not_one = segments_in_four - segments_in_one
    for i_digit, raw in enumerate(display["raw_displays"]):
        active_segments = set(raw)
        if active_segments == segments_in_one:
            display["decoded_displays"][i_digit] = 1
            count += 1
        elif active_segments == segments_in_four:
            display["decoded_displays"][i_digit] = 4
            count += 1
        elif active_segments == segments_in_seven:
            display["decoded_displays"][i_digit] = 7
            count += 1
        elif len(active_segments) == 7:
            display["decoded_displays"][i_digit] = 8
            count += 1
        elif len(active_segments) == 6:
            if segments_in_four.issubset(active_segments):
                display["decoded_displays"][i_digit] = 9
            elif segments_in_one.issubset( active_segments):
                display["decoded_displays"][i_digit] = 0
            else:
                display["decoded_displays"][i_digit] = 6
        # length must be 5
        else:
            if segments_in_one.issubset(active_segments):
                display["decoded_displays"][i_digit] = 3
            elif segments_in_four_but_not_one.issubset(active_segments):
                display["decoded_displays"][i_digit] = 5
            else:
                display["decoded_displays"][i_digit] = 2

total = sum([int("".join(map(str, d["decoded_displays"]))) for d in displays.values()])
print(f"Part 1: unique signal patters appear {count} times in the displays")
print(f"Part 2: sum of displays is {total}")


