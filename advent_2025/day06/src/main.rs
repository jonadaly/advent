use std::fs;

fn do_sum(args: &[i64], operation: char) -> i64 {
    match operation {
        '+' => args.iter().sum::<i64>(),
        '*' => args.iter().product::<i64>(),
        _ => panic!("Invalid operation: {}", operation),
    }
}
fn main() {
    let contents = fs::read_to_string("input.txt").expect("Could not read file");
    let lines: Vec<&str> = contents.lines().collect();
    let (operations_raw, data_raw) = lines.split_last().unwrap();
    let operations: Vec<char> = operations_raw
        .split_whitespace()
        .map(|s| s.chars().next().unwrap())
        .collect();

    let data_p1: Vec<Vec<i64>> = data_raw
        .iter()
        .map(|line| {
            line.split_whitespace()
                .map(|s| s.parse().unwrap())
                .collect()
        })
        .collect();
    let data_p2: Vec<Vec<char>> = lines.iter().map(|line| line.chars().collect()).collect();

    let mut total_p1 = 0;
    for (i, operation) in operations.into_iter().enumerate() {
        let operands_p1: Vec<i64> = data_p1.iter().map(|x| x[i]).collect();
        total_p1 += do_sum(&operands_p1, operation);
    }

    let mut total_p2 = 0;
    let mut current_sum_args: Vec<i64> = Vec::new();
    for i in (0..data_p2[0].len()).rev() {
        let raw_chars: Vec<char> = data_p2.iter().map(|x| x[i]).collect();
        if raw_chars.iter().all(|x| x.is_whitespace()) {
            continue;
        }
        let parsed_number = raw_chars[..raw_chars.len() - 1]
            .iter()
            .collect::<String>()
            .trim()
            .parse()
            .unwrap();
        current_sum_args.push(parsed_number);
        let operation = *raw_chars.last().unwrap();
        if operation != ' ' {
            total_p2 += do_sum(&current_sum_args, operation);
            current_sum_args.clear();
        }
    }

    println!("Part 1: Total is {}", total_p1); // 6891729672676
    println!("Part 2: Total is {}", total_p2); // 9770311947567
}
