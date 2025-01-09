use itertools::Itertools;
use std::{collections::HashMap, fs};

fn main() {
    let contents = fs::read_to_string("input.txt").expect("Could not read file");
    let (minimum, maximum) = contents
        .trim()
        .split("-")
        .map(|x| x.parse::<i32>().unwrap())
        .next_tuple()
        .unwrap();

    let mut p1_total = 0;
    let mut p2_total = 0;
    for candidate in minimum..=maximum {
        let candidate_str = candidate.to_string();
        let mut has_decreasing = false;
        let mut pairs: HashMap<char, i32> = HashMap::new();
        for (a, b) in candidate_str.chars().zip(candidate_str.chars().skip(1)) {
            if a == b {
                *pairs.entry(a).or_insert(0) += 1;
            }
            if a > b {
                has_decreasing = true;
                break;
            }
        }
        if !has_decreasing {
            if !pairs.is_empty() {
                p1_total += 1;
            }
            if pairs.values().any(|&x| x == 1) {
                p2_total += 1;
            }
        }

    }
    println!("Part 1: total number of possible passwords is {}", p1_total);
    println!("Part 2: total number of possible passwords is {}", p2_total);
}
