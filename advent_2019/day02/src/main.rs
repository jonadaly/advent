use std::fs;

// Run an intcode computer, and search for inputs that produce a desired output.

fn run_program(program: &[usize], noun: usize, verb: usize) -> usize {
    let mut mem = program.to_owned();
    mem[1] = noun;
    mem[2] = verb;

    let mut ptr = 0;
    loop {
        let opcode = mem[ptr];
        if opcode == 99 {
            return mem[0];
        }
        let param1 = mem[mem[ptr + 1]];
        let param2 = mem[mem[ptr + 2]];
        let dest = mem[ptr + 3];
        if opcode == 1 {
            mem[dest] = param1 + param2;
        } else if opcode == 2 {
            mem[dest] = param1 * param2;
        } else {
            panic!("unknown opcode {}", opcode);
        }
        ptr += 4;
    }
}
fn main() {
    let contents = fs::read_to_string("input.txt").expect("Could not read file");
    let program = contents
        .trim()
        .split(",")
        .map(|x| x.parse::<usize>().unwrap())
        .collect::<Vec<_>>();

    let result = run_program(&program, 12, 2);
    println!("Part 1: result is {}", result);

    for noun in 0..100 {
        for verb in 0..100 {
            let result = run_program(&program, noun, verb);
            if result == 19690720 {
                println!("Part 2: answer is {}", 100 * noun + verb);
                break;
            }
        }
    }
}
