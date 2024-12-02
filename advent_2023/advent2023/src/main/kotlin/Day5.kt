fun main() {
    val day = Day5()
    println("Part 1: answer is ${day.solvePart1()}")
    println("Part 2: answer is ${day.solvePart2()}")
}

class Day5 : BaseDay("/input5.txt") {

    override fun solvePart1(): Long {
        val (seeds, mappings) = parseInput(input)
        return solveFor(seeds, mappings)
    }

    override fun solvePart2(): Long {
        val (seeds, mappings) = parseInput(input)
//        // Seeds is now a list of alternating starting points and ranges. Convert it into a single list of seeds where
//        // we take the first and last value of each range. e.g. (start1, range1, start2, range2, ...) -> (start1, start1 + range1 - 1, start2, start2 + range2 - 1, ...)
//        val updatedSeeds = seeds.mapIndexed { index, seed ->
//            if (index % 2 == 0) seed else seed + seeds[index - 1] - 1
//        }
        // Seeds is now a list of alternating starting points and ranges. Convert it into a single list of seeds
        // e.g. (start1, range1, start2, range2, ...) -> (start1, start1 + 1, ... start1 + range1 -1, range2, range2 + 1, ...)
        val updatedSeeds = seeds.flatMapIndexed { index, seed ->
            if (index % 2 == 0) (seed..(seed + seeds[index + 1] - 1)).toList() else emptyList()
        }
        return solveFor(updatedSeeds, mappings)
    }

    private fun parseInput(input: String): Pair<List<Long>, List<List<Triple<Long, Long, Long>>>> {
        val seeds = input.lines().first().split(":")[1].trim().split(" ").map { it.toLong() }
        val sections = input.lines()
            .drop(2)
            .joinToString("\n")
            .split("\n\n")
            .map { section ->
                section
                    .split(":")[1]
                        .trim()
                        .split("\n")
                        .map{entry ->
                            entry.split(" ")
                                .let {
                                    Triple(it[0].toLong(), it[1].toLong(), it[2].toLong())
                                }
                    }
            }
        return Pair(seeds, sections)
    }

    private fun solveFor(seeds: List<Long>, mappings: List<List<Triple<Long, Long, Long>>>): Long {
        return seeds.minOf { seed ->
            var current = seed
            for (mapping in mappings) {
                for (entry in mapping) {
                    if (current in entry.second..<entry.second + entry.third) {
                        current = current - entry.second + entry.first
                        break
                    }
                }
            }
            println("Seed $seed -> $current")
            current
        }
    }
}