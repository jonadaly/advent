use std::fs;

const COORDS: [(isize, isize); 8] = [
    (-1, -1),
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0),
    (1, 1),
    (1, -1),
    (-1, 1),
];

fn count_adjacent(layout: &mut Vec<Vec<char>>, remove_in_place: bool) -> u32 {
    let mut sub_count = 0;
    for row in 0..layout.len() {
        for col in 0..layout[0].len() {
            if layout[row][col] == '.' {
                continue;
            }
            let mut total = 0;
            for coord in COORDS {
                let new_row = row as isize + coord.0;
                let new_col = col as isize + coord.1;
                if new_row < 0
                    || new_row >= layout.len() as isize
                    || new_col < 0
                    || new_col >= layout[0].len() as isize
                {
                    continue;
                }
                if layout[new_row as usize][new_col as usize] == '@' {
                    total += 1;
                }
            }
            if total < 4 {
                sub_count += 1;
                if remove_in_place {
                    layout[row][col] = '.';
                }
            }
        }
    }
    sub_count
}

fn main() {
    let contents = fs::read_to_string("input.txt").expect("Could not read file");
    let mut layout: Vec<Vec<char>> = contents.lines().map(|x| x.chars().collect()).collect();
    let count_p1 = count_adjacent(&mut layout, false);
    let mut count_p2 = 0;
    loop {
        let sub_count = count_adjacent(&mut layout, true);
        if sub_count == 0 {
            break;
        }
        count_p2 += sub_count;
    }
    println!("Part 1: count is {}", count_p1); // 1578
    println!("Part 2: count is {}", count_p2); // 10132
}
