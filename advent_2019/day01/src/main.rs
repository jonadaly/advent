use std::fs;

// Calculate fuel required to launch modules, taking weight of fuel into account.

fn calculate_fuel(mass: i32) -> i32 {
    mass / 3 - 2
}

fn calculate_fuel_recursive(mass: i32) -> i32 {
    let fuel = calculate_fuel(mass);
    if fuel <= 0 {
        return 0;
    }
    fuel + calculate_fuel_recursive(fuel)
}
fn main() {
    let contents = fs::read_to_string("input.txt").expect("Could not read file");
    let masses = contents.lines().map(|x| x.parse::<i32>().unwrap());

    let naive_fuel_sum = masses.clone().map(calculate_fuel).sum::<i32>();
    println!("Part 1: naive fuel sum is {}", naive_fuel_sum);

    let recursive_fuel_sum = masses.clone().map(calculate_fuel_recursive).sum::<i32>();
    println!("Part 2: recursive fuel sum is {}", recursive_fuel_sum);
}
