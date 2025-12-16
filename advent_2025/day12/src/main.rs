use regex::Regex;
use std::fs;

#[derive(Debug)]
struct Tile {
    shape: Vec<Vec<char>>,
    area: usize,
}

#[derive(Debug)]
struct Region {
    width: usize,
    length: usize,
    required_tiles: Vec<usize>,
}

fn main() {
    let region_regex = Regex::new(r"(\d+)x(\d+):\s+(.+)$").unwrap();
    let contents = fs::read_to_string("input.txt").expect("Could not read file");
    let raw_input: Vec<&str> = contents.split("\n\n").collect();
    let tiles: Vec<Tile> = raw_input[..raw_input.len() - 1]
        .to_vec()
        .iter()
        .map(|t| {
            let shape: Vec<Vec<char>> = t.lines().skip(1).map(|l| l.chars().collect()).collect();
            let area = shape.iter().flatten().filter(|c| **c == '#').count();
            Tile { shape, area }
        })
        .collect();
    let regions: Vec<Region> = raw_input
        .last()
        .unwrap()
        .lines()
        .map(|r| {
            let captures = region_regex.captures(r).unwrap();
            let width = captures[1].parse().unwrap();
            let length = captures[2].parse().unwrap();
            let required_tiles = captures[3]
                .split_whitespace()
                .map(|t| t.parse().unwrap())
                .collect();
            Region {
                width,
                length,
                required_tiles,
            }
        })
        .collect();

    // Try the naive way:
    let mut fit_yes_count = 0;
    let mut fit_no_count = 0;
    let mut fit_maybe_count = 0;
    for region in regions {
        // Ignoring tile shape, if the region isn't big enough to fit the area of the tiles, it's definitely a no.
        let min_space_required: usize = region
            .required_tiles
            .iter()
            .enumerate()
            .map(|(idx, num)| tiles[idx].area * num)
            .sum();
        let max_space_available: usize = region.width * region.length;
        if min_space_required > max_space_available {
            fit_no_count += 1;
            continue;
        }
        // If each tile has its own 3x3 space available, it's definitely a yes.
        let total_tiles = region.required_tiles.iter().sum::<usize>();
        if (region.width / 3) * (region.length / 3) >= total_tiles {
            fit_yes_count += 1;
            continue;
        }
        // Otherwise, we don't know for sure either way.
        fit_maybe_count += 1;
    }
    if fit_maybe_count == 0 {
        println!("Part 1: Number of regions that fit: {}", fit_yes_count);
    } else {
        println!(
            "Don't know - figure it out manually :) ({} yes, {} no, {} maybe)",
            fit_yes_count, fit_no_count, fit_maybe_count
        );
    }
}
