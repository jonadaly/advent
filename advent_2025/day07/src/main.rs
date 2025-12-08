use std::{collections::HashMap, fs};

fn count_routes_from(
    manifold: &Vec<Vec<char>>,
    current: (usize, usize),
    memo: &mut HashMap<(usize, usize), u64>,
    splitter_count: &mut u64,
) -> u64 {
    // Memoization saves us a lot of recalculating the same paths.
    if let Some(cached) = memo.get(&current) {
        return *cached;
    }
    if current.0 >= manifold.len() {
        // Reached bottom of manifold.
        memo.insert(current, 1);
        return 1;
    }
    if manifold[current.0][current.1] == '^' {
        // Reached a splitter, calculate for both paths.
        *splitter_count += 1;
        let left = count_routes_from(
            manifold,
            (current.0 + 1, current.1 - 1),
            memo,
            splitter_count,
        );
        let right = count_routes_from(
            manifold,
            (current.0 + 1, current.1 + 1),
            memo,
            splitter_count,
        );
        memo.insert(current, left + right);
        return left + right;
    }

    // Not a splitter, continue down.
    let paths = count_routes_from(manifold, (current.0 + 1, current.1), memo, splitter_count);
    memo.insert(current, paths);
    return paths;
}
fn main() {
    let contents = fs::read_to_string("input.txt").expect("Could not read file");
    let manifold: Vec<Vec<char>> = contents.lines().map(|x| x.chars().collect()).collect();
    let start_col: usize = manifold
        .first()
        .unwrap()
        .iter()
        .position(|x| *x == 'S')
        .unwrap();
    let start = (0, start_col);

    let mut memo = HashMap::new();
    let mut splitter_count = 0;
    let num_routes = count_routes_from(&manifold, start, &mut memo, &mut splitter_count);

    println!("Part 1: Split count: {}", splitter_count); // 1656
    println!("Part 2: Number of routes: {}", num_routes); //76624086587804
}
