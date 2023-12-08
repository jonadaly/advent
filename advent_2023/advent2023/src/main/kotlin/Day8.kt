

fun main() {
    val day8 = Day8()
    println("Part 1: total steps is ${day8.solvePart1()}")
    println("Part 2: winnings total is ${day8.solvePart2()}")
}

class Day8 : BaseDay("/input8.txt") {
    data class Node(val left: String, val right: String)

    override fun solvePart1(): Int {
        val (instructions, nodes) = parseDay8Input(input)
        return solve(instructions, nodes, "AAA", anyZ = false)
    }

    override fun solvePart2(): Long {
        // Same as part 1, but for X simultaneous games until they all simultaneously land on ZZZ.
        // We just need to find the lowest common multiple of the iterations from each starting point.
        val (instructions, nodes) = parseDay8Input(input)
        return nodes
            .filter { it.key.endsWith("A") } // Identify all starting nodes
            .map { solve(instructions, nodes, it.key, anyZ = true) } // Solve each starting node
            .map(Int::toLong)
            .reduce { acc, i -> findLcm(acc, i) } // Find LCM of total from each starting node
    }

    private fun parseDay8Input(input: String): Pair<String, Map<String, Node>> {
        val instructions = input.lines()[0]
        val nodes =
            input.lines().drop(2).mapNotNull { line ->
                "(.{3}) = \\((.{3}), (.{3})\\)".toRegex().find(line)?.groupValues?.let { it[1] to Node(it[2], it[3]) }
            }.toMap()
        return Pair(instructions, nodes)
    }

    private fun solve(
        instructions: String,
        nodes: Map<String, Node>,
        startNode: String,
        anyZ: Boolean,
    ): Int {
        var currentNodeId = startNode
        var counter = 0
        while (true) {
            val instruction = instructions[counter % instructions.length]
            val currentNode = nodes[currentNodeId]!!
            currentNodeId = if (instruction == 'L') currentNode.left else currentNode.right
            counter++
            if (currentNodeId == "ZZZ" || (anyZ && currentNodeId.endsWith("Z"))) return counter
        }
    }

    private fun findLcm(
        a: Long,
        b: Long,
    ): Long {
        // To find the lowest common multiple of two numbers, we can use the greatest common divisor.
        return a * b / findGcd(a, b)
    }

    private fun findGcd(
        a: Long,
        b: Long,
    ): Long {
        // To find the greatest common divisor, we can use Euclid's algorithm.
        if (b == 0L) return a
        return findGcd(b, a % b)
    }
}
