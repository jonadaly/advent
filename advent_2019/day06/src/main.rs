use std::{
    collections::{HashMap, HashSet},
    fs,
};

// Lifetime annotations are needed because we are moving data between multiple reference parameters (so they need to have the same lifetime).
fn get_orbits<'a>(
    body: &'a str,
    direct_orbits: &HashMap<&'a str, &'a str>,
    all_orbits: &mut HashMap<&'a str, HashSet<&'a str>>,
) {
    if !direct_orbits.contains_key(body) {
        all_orbits.insert(body, HashSet::from_iter(vec![body]));
        return;
    }
    let direct_orbit = direct_orbits[body];
    if !all_orbits.contains_key(direct_orbit) {
        get_orbits(&direct_orbit, direct_orbits, all_orbits);
    }
    let mut updated_orbits = all_orbits[direct_orbit].clone();
    updated_orbits.insert(body);
    all_orbits.insert(body, updated_orbits);
}

fn main() {
    let contents = fs::read_to_string("input.txt").expect("Could not read file");
    let direct_orbits: HashMap<&str, &str> = contents
        .lines()
        .map(|x| {
            let (orbitee, orbiter) = x.split_once(")").unwrap();
            (orbiter, orbitee)
        })
        .collect();
    let mut all_orbits = HashMap::new();
    for body in direct_orbits.keys() {
        get_orbits(body, &direct_orbits, &mut all_orbits);
    }
    let total_orbits = all_orbits.values().map(|x| x.len() - 1).sum::<usize>();
    println!("Part 1: There are {} total orbits", total_orbits);

    // Number of transits is equal to the number of bodies that are in exactly one of the two sets (minus you and santa)
    let transits = all_orbits["YOU"]
        .symmetric_difference(&all_orbits["SAN"])
        .count();
    println!(
        "Part 2: There are {} transfers between you and Santa",
        transits - 2
    );
}
