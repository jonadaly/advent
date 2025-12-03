use std::fs;

fn find_max_and_index(bank: &[u32]) -> (usize, u32) {
    let max_val = bank.iter().max().unwrap();
    let max_idx = bank.iter().position(|x| x == max_val).unwrap();
    (max_idx, *max_val)
}

fn calculate_joltage(bank: &[u32], batteries: usize) -> u128 {
    let mut start_idx = 0;
    let mut digits = Vec::new();
    for i in 0..batteries {
        let bank_slice = &bank[start_idx..bank.len() - (batteries - i - 1)];
        let (max_idx, max_val) = find_max_and_index(bank_slice);
        start_idx += max_idx + 1;
        digits.push(max_val);
    }
    // Combine digits into a single number.
    let number = digits
        .iter()
        .fold(0 as u128, |acc, elem| acc * 10 + *elem as u128);
    println!("number: {}", number);
    number
}

fn main() {
    let contents = fs::read_to_string("input.txt").expect("Could not read file");
    let banks: Vec<Vec<u32>> = contents
        .lines()
        .map(|x| x.chars().map(|c| c.to_digit(10).unwrap()).collect())
        .collect();
    let mut total_p1: u128 = 0;
    let mut total_p2: u128 = 0;
    for bank in banks {
        total_p1 += calculate_joltage(&bank, 2);
        total_p2 += calculate_joltage(&bank, 12);
    }
    println!("Part 1: joltage is {}", total_p1); // 16812
    println!("Part 2: joltage is {}", total_p2); // 166345822896410
}
