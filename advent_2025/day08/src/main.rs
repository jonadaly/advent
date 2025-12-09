use itertools::Itertools;
use std::collections::HashMap;
use std::fs;

type BoxCoord = (i64, i64, i64);

// A disjoint-set data structure stores a collection of non-overlapping sets, and allows for efficient merging.
// We store the parent of each node (initialized to itself), and the size of each set.
struct DisjointSet {
    parents: HashMap<BoxCoord, BoxCoord>,
    sizes: HashMap<BoxCoord, u32>,
}

impl DisjointSet {
    fn new(box_coordinates: &[BoxCoord]) -> Self {
        let length = box_coordinates.len();
        let mut parents = HashMap::with_capacity(length);
        let mut sizes = HashMap::with_capacity(length);
        for &coord in box_coordinates {
            parents.insert(coord, coord);
            sizes.insert(coord, 1);
        }
        Self { parents, sizes }
    }

    fn find(&mut self, my_box: &BoxCoord) -> BoxCoord {
        let parent = *self.parents.get(my_box).unwrap();
        if parent == *my_box {
            return *my_box;
        }
        // Optimization: path compression - connect to the root directly, to avoid unnecessary iteration later.
        let root = self.find(&parent);
        self.parents.insert(*my_box, root);
        root
    }

    fn merge(&mut self, box1: BoxCoord, box2: BoxCoord) {
        let root1 = self.find(&box1);
        let root2 = self.find(&box2);
        if root1 == root2 {
            return; // Already in same set
        }
        let size1 = *self.sizes.get(&root1).unwrap();
        let size2 = *self.sizes.get(&root2).unwrap();
        let new_size = size1 + size2;

        // Possible optimization: minimize tree depth by choosing the smaller tree to merge into the larger tree.
        self.parents.insert(root2, root1);
        self.sizes.insert(root1, new_size);
        self.sizes.remove(&root2);
    }
}

fn main() {
    let n = 1000;
    let contents = fs::read_to_string("input.txt").expect("Could not read file");
    let box_coordinates: Vec<BoxCoord> = contents
        .lines()
        .map(|x| {
            let parts: Vec<i64> = x.split(',').map(|y| y.parse().unwrap()).collect();
            (parts[0], parts[1], parts[2])
        })
        .collect();

    // Find distance between all pairs of boxes. Can use square distance as a proxy for euclidean distance (avoids sqrt)
    let mut square_distances = Vec::new();
    for (c1, c2) in box_coordinates.iter().tuple_combinations() {
        let square_distance = (c1.0 - c2.0).pow(2) + (c1.1 - c2.1).pow(2) + (c1.2 - c2.2).pow(2);
        square_distances.push(((*c1, *c2), square_distance));
    }
    square_distances.sort_by_key(|(_, d)| *d);

    let mut circuits = DisjointSet::new(&box_coordinates);
    let mut i = 0;
    loop {
        let pair = square_distances[i].0;
        circuits.merge(pair.0, pair.1);

        if i == n {
            let product_top3: u32 = circuits
                .sizes
                .values()
                .copied()
                .sorted_by(|a, b| b.cmp(a))
                .take(3)
                .product();
            println!("Part 1: Product of top 3 sizes is {}", product_top3); // 103488
        }
        i += 1;

        if circuits.sizes.len() == 1 {
            // We've made it to one large circuit.
            println!("Part 2: Wall distance is {}", pair.0 .0 * pair.1 .0); // 8759985540
            break;
        }
    }
}
