use itertools::Itertools;
use std::fs;

// Use the intcode computer to calculate the output of chained amplifiers.

struct Amplifier {
    memory: Vec<i64>,
    phase_setting: i64,
    initialized: bool,
    instruction_ptr: usize,
}

impl Amplifier {
    fn build(program: &[i64], phase_setting: i64) -> Self {
        Amplifier {
            memory: program.to_owned(),
            phase_setting,
            initialized: false,
            instruction_ptr: 0,
        }
    }

    // Sadly the intcode computer is slightly different from previous days, so we need to duplicate it here.
    fn run(&mut self, input: i64) -> Option<i64> {
        loop {
            let instruction_code = self.memory[self.instruction_ptr];

            macro_rules! param {
                // Get the parameter at position $pos, either by value or by address based on the "mode".
                ($pos:literal) => {{
                    let mode = instruction_code / 10i64.pow($pos as u32 + 1) % 10;
                    let param = self.memory[self.instruction_ptr + $pos];
                    if mode == 0 {
                        self.memory[param as usize]
                    } else {
                        param
                    }
                }};
            }

            macro_rules! set_memory_to {
            // Set memory at position $pos to output of expression $e.
            ($pos:literal, $e:expr) => {
                let dest = self.memory[self.instruction_ptr + $pos] as usize;
                self.memory[dest] = $e;
            };
        }

            let opcode = instruction_code % 100;
            match opcode {
                1 => {
                    set_memory_to!(3, param!(1) + param!(2));
                    self.instruction_ptr += 4;
                }
                2 => {
                    set_memory_to!(3, param!(1) * param!(2));
                    self.instruction_ptr += 4;
                }
                3 => {
                    if self.initialized {
                        set_memory_to!(1, input);
                    } else {
                        set_memory_to!(1, self.phase_setting);
                        self.initialized = true;
                    }
                    self.instruction_ptr += 2;
                }
                4 => {
                    let output = param!(1);
                    self.instruction_ptr += 2;
                    return Some(output);
                }
                5 => {
                    if param!(1) != 0 {
                        self.instruction_ptr = param!(2) as usize
                    } else {
                        self.instruction_ptr += 3
                    };
                }
                6 => {
                    if param!(1) == 0 {
                        self.instruction_ptr = param!(2) as usize
                    } else {
                        self.instruction_ptr += 3
                    };
                }
                7 => {
                    set_memory_to!(3, (param!(1) < param!(2)) as i64);
                    self.instruction_ptr += 4;
                }
                8 => {
                    set_memory_to!(3, (param!(1) == param!(2)) as i64);
                    self.instruction_ptr += 4;
                }
                99 => return None,
                _ => panic!("unknown opcode {}", opcode),
            }
        }
    }
}

fn calculate_output(setting: &[i64], program: &[i64], is_feedback_enabled: bool) -> i64 {
    let mut amplifiers: Vec<Amplifier> = setting
        .into_iter()
        .map(|&s| Amplifier::build(&program, s))
        .collect();
    let mut current = 0;
    loop {
        for amp in &mut amplifiers {
            if let Some(output) = amp.run(current) {
                current = output;
            } else {
                return current;
            }
        }
        if !is_feedback_enabled {
            return current;
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

    let max_signal_p1 = { 0..=4 }
        .permutations(5)
        .map(|setting| calculate_output(&setting, &program, false))
        .max()
        .unwrap();
    println!("Part 1: max signal is {}", max_signal_p1);

    let max_signal_p2 = { 5..=9 }
        .permutations(5)
        .map(|setting| calculate_output(&setting, &program, true))
        .max()
        .unwrap();
    println!("Part 2: max signal with feedback is {}", max_signal_p2);
}
