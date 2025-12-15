use itertools::Itertools;
use regex::Regex;
use std::{collections::HashMap, fs};

/// I originally solved part 1 with a BFS, but needed a lot of help to figure out a solution for part 2.
/// https://www.reddit.com/r/adventofcode/comments/1pk87hl/2025_day_10_part_2_bifurcate_your_way_to_victory/

struct Machine {
    desired_lights: Vec<bool>,
    buttons: Vec<Vec<usize>>,
    desired_joltages: Vec<usize>,
}

fn find_all_patterns_with_cost(
    buttons: &[Vec<usize>],
    num_vars: usize,
) -> HashMap<Vec<usize>, usize> {
    // Insight: it's only worth pressing each button 0 or 1 times (2 is the same as 0).
    let mut patterns = HashMap::new();
    for num_pressed in 0..=buttons.len() {
        for indices in (0..buttons.len()).combinations(num_pressed) {
            let mut pattern = vec![0; num_vars];
            for i in indices {
                for &light in &buttons[i] {
                    pattern[light] += 1;
                }
            }
            // Cost is the number of button presses required.
            patterns.entry(pattern).or_insert(num_pressed);
        }
    }
    patterns
}

fn solve_recursive(
    target: &[usize],
    all_patterns: &HashMap<Vec<usize>, usize>,
    memo: &mut HashMap<Vec<usize>, usize>,
) -> usize {
    if target.iter().all(|x| *x == 0) {
        // We got to the target, no more button presses needed.
        return 0;
    }
    if let Some(cached) = memo.get(target) {
        return *cached;
    }
    let mut solution = usize::MAX;
    for (pattern, cost) in all_patterns {
        // Check we haven't gone too far, and that the parity is the same as the target.
        let valid = pattern
            .iter()
            .zip(target.iter())
            .all(|(&p, &g)| p <= g && p % 2 == g % 2);
        if valid {
            // Subtract pattern from target, divide by 2 (see Reddit post for explanation)
            let new_target: Vec<usize> = pattern
                .iter()
                .zip(target)
                .map(|(&p, &g)| (g - p) / 2)
                .collect();
            let sub_solution = solve_recursive(&new_target, all_patterns, memo);
            if sub_solution < usize::MAX {
                solution = solution.min(cost + 2 * sub_solution);
            }
        }
    }
    memo.insert(target.to_vec(), solution);
    solution
}

fn main() {
    let contents = fs::read_to_string("input.txt").expect("Could not read file");
    let machine_regex = Regex::new(r"\[([.#]+)\]\s+(.+?)\s+\{([0-9,]+)\}").unwrap();
    let machines: Vec<Machine> = contents
        .lines()
        .map(|line| {
            let machine_raw = machine_regex.captures(line).unwrap();
            let lights = machine_raw[1].chars().map(|c| c == '#').collect();
            let buttons = machine_raw[2]
                .split_whitespace()
                .map(|b| {
                    b[1..b.len() - 1]
                        .split(',')
                        .map(|c| c.parse().unwrap())
                        .collect()
                })
                .collect();
            let desired_joltages = machine_raw[3]
                .split(',')
                .map(|j| j.parse().unwrap())
                .collect();
            Machine {
                desired_lights: lights,
                buttons: buttons,
                desired_joltages: desired_joltages,
            }
        })
        .collect();

    let mut total_button_presses_p1 = 0;
    let mut total_button_presses_p2 = 0;
    for machine in machines {
        let all_patterns =
            find_all_patterns_with_cost(&machine.buttons, machine.desired_lights.len());
        let button_presses_p1 = all_patterns
            .iter()
            .filter(|(pattern, _)| {
                pattern
                    .iter()
                    .map(|p| p % 2 == 1)
                    .eq(machine.desired_lights.iter().copied())
            })
            .map(|(_, &cost)| cost)
            .min()
            .unwrap();

        total_button_presses_p1 += button_presses_p1;
        let mut memo = HashMap::new();
        let button_presses_p2 = solve_recursive(&machine.desired_joltages, &all_patterns, &mut memo);
        total_button_presses_p2 += button_presses_p2;
    }
    println!("Part 1: Total button presses: {}", total_button_presses_p1); // 477
    println!("Part 2: Total button presses: {}", total_button_presses_p2); // 17970
}
