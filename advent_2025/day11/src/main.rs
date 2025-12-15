use std::{collections::HashMap, fs};

fn count_paths<'a>(
    connections: &'a HashMap<&'a str, Vec<&'a str>>,
    start: &'a str,
    end: &'a str,
    memo: &mut HashMap<(&'a str, &'a str), usize>,
) -> usize {
    let key = (start, end);
    if let Some(&cached) = memo.get(&key) {
        return cached;
    }
    if start == end {
        memo.insert(key, 1);
        return 1;
    }
    let mut count = 0;
    for child in connections.get(start).unwrap_or(&vec![]) {
        count += count_paths(connections, child, end, memo);
    }
    memo.insert(key, count);
    count
}

fn main() {
    let contents = fs::read_to_string("input.txt").expect("Could not read file");
    let connections: HashMap<&str, Vec<&str>> = contents
        .lines()
        .map(|line| {
            let (from, to) = line.split_once(": ").unwrap();
            (from, to.split_whitespace().collect())
        })
        .collect();
    let mut memo = HashMap::new();
    let possible_paths_p1 = count_paths(&connections, "you", "out", &mut memo);
    println!("Part 1: Number of possible paths is {}", possible_paths_p1); // 613

    // Input has to be a DAG for part 2 to work (otherwise you'd have loops), so can just figure out each path separately.
    let first = count_paths(&connections, "svr", "fft", &mut memo);
    let second = count_paths(&connections, "fft", "dac", &mut memo);
    let third = count_paths(&connections, "dac", "out", &mut memo);
    let possible_paths_p2 = first * second * third;
    println!("Part 2: Number of possible paths is {}", possible_paths_p2); // 372918445876116
}
