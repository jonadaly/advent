use std::fs;

fn has_repeating_chunks(id_str: &str, chunk_size: usize) -> bool {
    // If all subsequent chunks are equal to chunk1, then id is invalid.
    let chunk1 = id_str[..chunk_size].to_string();
    for chunk_idx in 1..id_str.len() / chunk_size {
        let chunk2 = id_str[chunk_idx * chunk_size..(chunk_idx + 1) * chunk_size].to_string();
        if chunk2 != chunk1 {
            return false;
        }
    }
    return true;
}
fn main() {
    let contents = fs::read_to_string("input.txt").expect("Could not read file");
    let ranges: Vec<(u64, u64)> = contents
        .trim()
        .split(',')
        .map(|x| {
            let parts: Vec<&str> = x.split('-').collect();
            (parts[0].parse().unwrap(), parts[1].parse().unwrap())
        })
        .collect();

    let mut p1_sum = 0;
    let mut p2_sum = 0;
    for range in ranges {
        for id in range.0..range.1 + 1 {
            let id_str = id.to_string();
            let length = id_str.len();
            let factors: Vec<usize> = (1..length / 2 + 1).filter(|x| length % x == 0).collect();
            for chunk_size in factors {
                if has_repeating_chunks(&id_str, chunk_size) {
                    if length / chunk_size == 2 {
                        p1_sum += id;
                    }
                    p2_sum += id;
                }
            }
        }
    }
    println!("Part 1: sum of invalid numbers is {}", p1_sum); // 56603486841
    println!("Part 2: sum of valid numbers is {}", p2_sum); // 79183223243
}
