use std::{
    collections::{HashMap, HashSet},
    fs,
};

// Calculate the paths of wires, where they cross and the distance to the first crossing.

fn parse_wire(wire: &[&str]) -> Vec<(i32, i32)> {
    let mut coords = vec![(0, 0)];
    for step in wire {
        let last_coord = coords.last().unwrap().clone();
        let (dir_str, dist_str) = step.split_at(1);
        let distance = dist_str.parse::<i32>().unwrap();
        let (dx, dy) = match dir_str {
            "L" => (-1, 0),
            "R" => (1, 0),
            "U" => (0, 1),
            "D" => (0, -1),
            _ => panic!("Unknown direction {}", dir_str),
        };
        for i in 1..=distance {
            coords.push((last_coord.0 + i * dx, last_coord.1 + i * dy));
        }
    }
    coords
}
fn main() {
    let contents = fs::read_to_string("input.txt").expect("Could not read file");
    let wires = contents
        .trim()
        .lines()
        .map(|x| x.split(",").collect::<Vec<_>>())
        .collect::<Vec<_>>();

    let coords1 = parse_wire(&wires[0]);
    let coords2 = parse_wire(&wires[1]);

    let set1: HashSet<_> = coords1.iter().skip(1).copied().collect();
    let set2: HashSet<_> = coords2.iter().skip(1).copied().collect();
    let crossings = set1.intersection(&set2);

    let closest_crossing = crossings
        .clone()
        .map(|&(x, y)| x.abs() + y.abs())
        .min()
        .unwrap();

    println!("Part 1: closet crossing is {}", closest_crossing);

    let mut crossings_with_distances: HashMap<(i32, i32), i32> = HashMap::new();
    for crossing in crossings {
        let steps1 = coords1.iter().position(|&x| x == *crossing).unwrap() as i32;
        let steps2 = coords2.iter().position(|&x| x == *crossing).unwrap() as i32;
        crossings_with_distances.insert(crossing.clone(), steps1 + steps2);
    }
    let min_crossing_steps = crossings_with_distances.values().min().unwrap();
    println!("Part 2: minimum steps to cross is {}", min_crossing_steps);
}
