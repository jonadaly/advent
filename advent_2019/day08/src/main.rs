use itertools::Itertools;
use std::fs;

// Parse a list of pixel values into layers, and figure out the final image after combining layers.

fn main() {
    let contents = fs::read_to_string("input.txt").expect("Could not read file");
    let width = 25;
    let height = 6;

    let layers: Vec<String> = contents
        .trim()
        .chars()
        .chunks(width * height)
        .into_iter()
        .map(|chunk| chunk.collect())
        .collect();

    let fewest_zeros = layers
        .iter()
        .min_by_key(|l| l.chars().filter(|&c| c == '0').count())
        .unwrap();
    let score = fewest_zeros.chars().filter(|&c| c == '1').count()
        * fewest_zeros.chars().filter(|&c| c == '2').count();

    println!("Part 1: layer score is {:?}", score);

    let pixels: String = (0..width * height)
        .map(|x| {
            layers
                .iter()
                .map(|l| l.chars().nth(x).unwrap())
                .find(|&c| c != '2')
                .unwrap()
        })
        .collect();

    let final_image: Vec<String> = pixels
        .chars()
        .chunks(width)
        .into_iter()
        .map(|chunk| chunk.collect())
        .collect();

    println!("Part 2: final image is:");
    for row in final_image {
        println!("{}", row.replace("0", ".").replace("1", "█"));
    }
}
