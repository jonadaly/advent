import re
from copy import copy
from pathlib import Path

report_values_raw = Path("03.txt").read_text().strip().split("\n")

N_DIGITS = len(report_values_raw[0])
N_VALUES = len(report_values_raw)


def count_ones(values_list, index):
    return len([1 for v in values_list if v[index] == "1"])


gamma_rate_totals = ["0" for _ in range(N_DIGITS)]
epsilon_rate_totals = ["0" for _ in range(N_DIGITS)]
for d in range(N_DIGITS):
    n_ones = count_ones(report_values_raw, d)
    gamma_rate_totals[d] = "1" if n_ones > (N_VALUES / 2) else "0"
    epsilon_rate_totals[d] = "0" if n_ones > (N_VALUES / 2) else "1"


gamma_rate = "".join(gamma_rate_totals)
epsilon_rate = "".join(epsilon_rate_totals)
print(
    f"Part 1: gamma rate is {gamma_rate}, epsilon rate is {epsilon_rate}, product is {int(gamma_rate, 2)*int(epsilon_rate, 2)}"
)


bit_pointer = 0
working_values = copy(report_values_raw)
while True:
    print(f"bit pointer {bit_pointer}, {len(working_values)} working_values left")
    n_ones = count_ones(working_values, bit_pointer)
    most_common_bit = "0" if n_ones < (len(working_values) / 2) else "1"
    working_values = [v for v in working_values if v[bit_pointer] == most_common_bit]
    if len(working_values) == 1:
        break
    bit_pointer += 1
o2_generator_rating = working_values[0]

bit_pointer = 0
working_values = copy(report_values_raw)
while True:
    print(f"bit pointer {bit_pointer}, {len(working_values)} working_values left")
    n_ones = count_ones(working_values, bit_pointer)
    least_common_bit = "1" if n_ones < (len(working_values) / 2) else "0"
    working_values = [v for v in working_values if v[bit_pointer] == least_common_bit]
    if len(working_values) == 1:
        break
    bit_pointer += 1
co2_scrubber_rating = working_values[0]
print(
    f"Part 2: O2 generator rating is {o2_generator_rating}, C02 scrubber rating is {co2_scrubber_rating}, product is {int(o2_generator_rating, 2) * int(co2_scrubber_rating, 2)}"
)
