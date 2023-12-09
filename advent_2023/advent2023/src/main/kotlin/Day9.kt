fun main() {
    val day = Day9()
    println("Part 1: answer is ${day.solvePart1()}")
    println("Part 2: answer is ${day.solvePart2()}")
}

class Day9 : BaseDay("/input9.txt") {
    override fun solvePart1(): Int {
        val sequences = parseInput(input)
        // Need to get list of last elements and add them up. Returning null in generateSequence will terminate it.
        return sequences.sumOf { sequence ->
            generateSequence(sequence) { curr ->
                val next = curr.zipWithNext { a, b -> b - a }
                if (next.any { it != 0 }) next else null
            }.sumOf { it.last() }
        }
    }

    override fun solvePart2(): Int {
        val sequences = parseInput(input)
        // Only difference is here we have to get a list of first elements and then do a - (b - (c - d)))
        return sequences.sumOf { sequence ->
            generateSequence(sequence) { curr ->
                val next = curr.zipWithNext { a, b -> b - a }
                if (next.any { it != 0 }) next else null
            }.map { it.first() }.toList().reversed().reduce { a, b -> b - a }
        }
    }

    private fun parseInput(input: String): List<List<Int>> {
        return input.lines().map { line -> line.split(" ").map { it.toInt() } }
    }
}
