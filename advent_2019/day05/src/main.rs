use std::fs;

// Run an intcode computer, with parameter "modes" and new opcodes.

fn run_program(program: &[i64], some_input: i64) -> i64 {
    let mut mem = program.to_owned();
    let mut ptr = 0;
    let mut output = 0;
    loop {
        let instruction_code = mem[ptr];

        macro_rules! param {
            // Get the parameter at position $pos, either by value or by address based on the "mode".
            ($pos:literal) => {{
                let mode = instruction_code / 10i64.pow($pos as u32 + 1) % 10;
                let param = mem[ptr + $pos];
                if mode == 0 {
                    mem[param as usize]
                } else {
                    param
                }
            }};
        }

        macro_rules! set_memory_to {
            // Set memory at position $pos to output of expression $e.
            ($pos:literal, $e:expr) => {
                let dest = mem[ptr + $pos] as usize;
                mem[dest] = $e;
            };
        }

        let opcode = instruction_code % 100;
        match opcode {
            1 => {
                set_memory_to!(3, param!(1) + param!(2));
                ptr += 4;
            }
            2 => {
                set_memory_to!(3, param!(1) * param!(2));
                ptr += 4;
            }
            3 => {
                set_memory_to!(1, some_input);
                ptr += 2;
            }
            4 => {
                output = param!(1);
                ptr += 2;
            }
            5 => {
                if param!(1) != 0 {
                    ptr = param!(2) as usize
                } else {
                    ptr += 3
                };
            }
            6 => {
                if param!(1) == 0 {
                    ptr = param!(2) as usize
                } else {
                    ptr += 3
                };
            }
            7 => {
                set_memory_to!(3, (param!(1) < param!(2)) as i64);
                ptr += 4;
            }
            8 => {
                set_memory_to!(3, (param!(1) == param!(2)) as i64);
                ptr += 4;
            }
            99 => return output,
            _ => panic!("unknown opcode {}", opcode),
        }
    }
}

fn main() {
    let contents = fs::read_to_string("input.txt").expect("Could not read file");
    let program = contents
        .trim()
        .split(",")
        .map(|x| x.parse::<i64>().unwrap())
        .collect::<Vec<_>>();

    let result_p1 = run_program(&program, 1);
    println!("Part 1: {}", result_p1);

    let result_p2 = run_program(&program, 5);
    println!("Part 2: {}", result_p2);
}
