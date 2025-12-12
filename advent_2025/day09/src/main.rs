use itertools::Itertools;
use std::fs;

fn is_box_fully_inside(
    corner1: (i64, i64),
    corner2: (i64, i64),
    vertical_edges: &[((i64, i64), (i64, i64))],
    horizontal_edges: &[((i64, i64), (i64, i64))],
) -> bool {
    let x_min = corner1.0.min(corner2.0);
    let x_max = corner1.0.max(corner2.0);
    let y_min = corner1.1.min(corner2.1);
    let y_max = corner1.1.max(corner2.1);

    // Box is not fully inside if any vertical or horizontal edge crosses through the box interior.
    for (c1, c2) in vertical_edges {
        let edge_x = c1.0.min(c2.0);
        let edge_y_min = c1.1.min(c2.1);
        let edge_y_max = c1.1.max(c2.1);
        if x_min < edge_x && edge_x < x_max && edge_y_min < y_max && edge_y_max > y_min {
            return false;
        }
    }

    for (c1, c2) in horizontal_edges {
        let edge_y = c1.1.min(c2.1);
        let edge_x_min = c1.0.min(c2.0);
        let edge_x_max = c1.0.max(c2.0);
        if y_min < edge_y && edge_y < y_max && edge_x_min < x_max && edge_x_max > x_min {
            return false;
        }
    }

    true
}

fn main() {
    let contents = fs::read_to_string("input.txt").expect("Could not read file");
    let coordinates: Vec<(i64, i64)> = contents
        .lines()
        .map(|line| {
            let (x, y) = line.split_once(",").unwrap();
            (x.parse().unwrap(), y.parse().unwrap())
        })
        .collect();

    let mut vertical_edges: Vec<((i64, i64), (i64, i64))> = Vec::new();
    let mut horizontal_edges: Vec<((i64, i64), (i64, i64))> = Vec::new();

    for i in 0..coordinates.len() {
        let c1 = coordinates[i];
        let c2 = coordinates[(i + 1) % coordinates.len()];
        if c1.0 == c2.0 {
            vertical_edges.push((c1, c2));
        } else if c1.1 == c2.1 {
            horizontal_edges.push((c1, c2));
        } else {
            panic!("Invalid coordinate pair: {:?} and {:?}", c1, c2);
        }
    }

    let mut max_area_p1 = 0;
    let mut max_area_p2 = 0;
    for (c1, c2) in coordinates.iter().tuple_combinations() {
        let area = ((c1.0 - c2.0).abs() + 1) * ((c1.1 - c2.1).abs() + 1);
        if area > max_area_p1 {
            max_area_p1 = area;
        }
        if area > max_area_p2 && is_box_fully_inside(*c1, *c2, &vertical_edges, &horizontal_edges) {
            max_area_p2 = area;
        }
    }
    println!("Part 1: Max area: {}", max_area_p1); // 4735222687
    println!("Part 2: Max area: {}", max_area_p2); // 1569262188
}
