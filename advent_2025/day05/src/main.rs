use itertools::Itertools;
use std::{collections::HashMap, fs};

fn is_fresh(ranges: &HashMap<u64, (u64, u64)>, id: u64) -> bool {
    ranges.values().any(|range| id >= range.0 && id <= range.1)
}

fn simplify_ranges(ranges: &HashMap<u64, (u64, u64)>) -> HashMap<u64, (u64, u64)> {
    let mut simplified_ranges = ranges.clone();
    let keys: Vec<u64> = ranges.keys().copied().collect();
    // Iterate through pairs of ranges a look for overlap. If found, simplify to one range.
    for (i, j) in keys.iter().tuple_combinations() {
        let overlap_start = simplified_ranges[i].0.max(simplified_ranges[j].0);
        let overlap_end = simplified_ranges[i].1.min(simplified_ranges[j].1);
        if overlap_start <= overlap_end {
            let min_start = simplified_ranges[i].0.min(simplified_ranges[j].0);
            let max_end = simplified_ranges[i].1.max(simplified_ranges[j].1);
            simplified_ranges.insert(*i, (min_start, max_end));
            simplified_ranges.remove(j);
            break;
        }
    }
    simplified_ranges
}

fn main() {
    let contents = fs::read_to_string("input.txt").expect("Could not read file");
    let (ranges_raw, ids_raw) = contents.split_once("\n\n").unwrap();
    let mut ranges: HashMap<u64, (u64, u64)> = ranges_raw
        .lines()
        .enumerate()
        .map(|(i, x)| {
            let (start, end) = x.split_once("-").unwrap();
            (
                i as u64,
                (start.parse().unwrap(), end.parse().unwrap()),
            )
        })
        .collect();

    let ids: Vec<u64> = ids_raw.lines().map(|x| x.parse::<u64>().unwrap()).collect();
    let fresh_count_p1 = ids.into_iter().filter(|&id| is_fresh(&ranges, id)).count();

    loop {
        let len_before = ranges.len();
        ranges = simplify_ranges(&ranges);
        if ranges.len() == len_before {
            break;
        }
    }
    let fresh_count_p2 = ranges.values().map(|x| x.1 - x.0 + 1).sum::<u64>();

    println!("Part 1: {}", fresh_count_p1); //520
    println!("Part 2: {}", fresh_count_p2); // 347338785050515
}
