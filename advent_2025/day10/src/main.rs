use regex::Regex;
use std::{
    collections::{HashSet, VecDeque},
    fs,
};

struct Machine {
    desired_lights: Vec<bool>,
    buttons: Vec<Vec<usize>>,
    desired_joltages: Vec<usize>,
}

fn simplify(state: &[usize]) -> Vec<bool> {
    state.iter().map(|x| x % 2 == 1).collect()
}

fn bfs(machine: &Machine) -> Option<usize> {
    let initial: Vec<usize> = vec![0; machine.desired_lights.len()];
    let mut visited = HashSet::new();
    let mut queue = VecDeque::from([(initial, 0)]);

    while let Some((state, depth)) = queue.pop_front() {
        if !visited.insert(simplify(&state)) {
            continue;
        }
        for button in &machine.buttons {
            let mut next = state.clone();
            for &light in button {
                next[light] += 1;
            }
            if simplify(&next) == machine.desired_lights {
                return Some(depth + 1);
            }
            queue.push_back((next, depth + 1));
        }
    }
    None
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

    let mut total_button_presses = 0;
    for machine in machines {
        let steps_p1 = bfs(&machine).unwrap();
        total_button_presses += steps_p1;
    }
    println!("Part 1: Total button presses: {}", total_button_presses);
}
