use std::fs;

fn rotate(start: i32, count: i32) -> (i32, i32) {
    // Rust's % operator is remainder not modulo, so we need to handle negative numbers.
    let position = ((start + count) % 100 + 100) % 100;

    if count >= 0 {
        // Moving right.
        let clicks = (start + count) / 100;
        return (position, clicks);
    }

    // Moving left.
    if start + count > 0 {
        // We never cross.
        return (position, 0);
    }

    // Count how many times we cross 0 going left - watch out for when we start at 0.
    let mut clicks = -(count + start) / 100;
    if start != 0 {
        clicks += 1
    };
    return (position, clicks);
}

fn main() {
    let contents = fs::read_to_string("input.txt").expect("Could not read file");
    let instructions = contents
        .lines()
        .map(|x| (x.chars().nth(0).unwrap(), x[1..].parse::<i32>().unwrap()))
        .collect::<Vec<_>>();

    let mut current = 50;
    let mut part1_count = 0;
    let mut part2_count = 0;
    for (direction, amount) in instructions {
        let rotation = match direction {
            'R' => amount,
            'L' => -amount,
            _ => panic!("Invalid direction"),
        };
        let (position, clicks) = rotate(current, rotation);
        part2_count += clicks;
        current = position;
        if current == 0 {
            part1_count += 1;
        }
    }
    println!("Part 1: {}", part1_count); // 1029
    println!("Part 2: {}", part2_count); // 5892
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_rotate() {
        assert_eq!(rotate(50, -68), (82, 1));
        assert_eq!(rotate(82, -30), (52, 0));
        assert_eq!(rotate(52, 48), (0, 1));
        assert_eq!(rotate(0, -5), (95, 0));
        assert_eq!(rotate(95, 60), (55, 1));
        assert_eq!(rotate(55, -55), (0, 1));
        assert_eq!(rotate(0, -1), (99, 0));
        assert_eq!(rotate(99, -99), (0, 1));
        assert_eq!(rotate(0, 14), (14, 0));
        assert_eq!(rotate(14, -82), (32, 1));
        assert_eq!(rotate(50, 1000), (50, 10));
        assert_eq!(rotate(0, 100), (0, 1));
        assert_eq!(rotate(0, 200), (0, 2));
        assert_eq!(rotate(50, -150), (0, 2));
    }
}
