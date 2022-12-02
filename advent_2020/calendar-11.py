from pathlib import Path

import numpy as np


def print_area(area):
    temp_cav = np.copy(area)
    for row in temp_cav:
        print(row.tostring().decode("utf8"))


raw_area = Path("11.txt").read_text().strip().split("\n")

width = len(raw_area[0])
height = len(raw_area)
area = np.chararray((height, width), itemsize=1)
for ind, row in enumerate(raw_area):
    area[ind, :] = list(row)

print_area(area)
print("=" * 20)

# # Part 1
# while True:
#     new_area = np.copy(area)
#     for i_row, row in enumerate(area):
#         for i_col, element in enumerate(row):
#             start_row = max(i_row - 1, 0)
#             end_row = min(i_row + 2, height)
#             start_col = max(i_col - 1, 0)
#             end_col = min(i_col + 2, width)
#             local = area[start_row:end_row, start_col:end_col]
#             if element == b"L" and b"#" not in local:
#                 new_area[i_row, i_col] = b"#"
#             if element == b"#" and np.sum(local == b"#") > 4:
#                 new_area[i_row, i_col] = b"L"
#     if np.array_equal(area, new_area):
#         break
#     area = new_area
#     # print_area(area)
#     # print("="*20)
# print_area(area)
# print("="*20)
# occupied = np.sum(area == b"#")
# print(f"Part 1: {occupied} occupied seats")

# Part 2
while True:
    new_area = np.copy(area)
    for i_row, row in enumerate(area):
        for i_col, element in enumerate(row):

            N = np.flip(area[:i_row, i_col])
            S = area[i_row + 1 :, i_col]
            E = area[i_row, i_col + 1 :]
            W = np.flip(area[i_row, :i_col])
            NE = np.diag(np.flipud(area[:i_row, i_col + 1 :]))
            SE = np.diag(area[i_row + 1 :, i_col + 1 :])
            NW = np.diag(np.flipud(np.fliplr(area[:i_row, :i_col])))
            SW = np.diag(np.fliplr(area[i_row + 1 :, :i_col]))

            N_first_occupied = next((n for n in N if n != b"."), None) == b"#"
            S_first_occupied = next((n for n in S if n != b"."), None) == b"#"
            E_first_occupied = next((n for n in E if n != b"."), None) == b"#"
            W_first_occupied = next((n for n in W if n != b"."), None) == b"#"
            NE_first_occupied = next((n for n in NE if n != b"."), None) == b"#"
            SE_first_occupied = next((n for n in SE if n != b"."), None) == b"#"
            NW_first_occupied = next((n for n in NW if n != b"."), None) == b"#"
            SW_first_occupied = next((n for n in SW if n != b"."), None) == b"#"

            occupied_surrounding = [
                N_first_occupied,
                S_first_occupied,
                E_first_occupied,
                W_first_occupied,
                NE_first_occupied,
                SE_first_occupied,
                NW_first_occupied,
                SW_first_occupied,
            ]

            # print(f"N: occupied {N_first_occupied} {N}")
            # print(f"S: occupied {S_first_occupied} {S}")
            # print(f"E: occupied {E_first_occupied} {E}")
            # print(f"W: occupied {W_first_occupied} {W}")
            # print(f"NE: occupied {NE_first_occupied} {NE}")
            # print(f"SE: occupied {SE_first_occupied} {SE}")
            # print(f"NW: occupied {NW_first_occupied} {NW}")
            # print(f"SW: occupied {SW_first_occupied} {SW}")

            if element == b"L" and not any(occupied_surrounding):
                new_area[i_row, i_col] = b"#"
            if element == b"#" and sum(occupied_surrounding) > 4:
                new_area[i_row, i_col] = b"L"
    if np.array_equal(area, new_area):
        break
    area = new_area
    # print_area(area)
    # print("="*20)
print_area(area)
print("=" * 20)
occupied = np.sum(area == b"#")
print(f"Part 1: {occupied} occupied seats")
