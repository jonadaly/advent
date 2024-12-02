fun main() {
    val day = Day10()
    println("Part 1: answer is ${day.solvePart1()}")
    println("Part 2: answer is ${day.solvePart2()}")
}

class Day10 : BaseDay("/input10.txt") {

    override fun solvePart1(): Int {
        val map = input.lines().map { it.toCharArray() }
        // Find the "S" in the map
        var current = map.mapIndexed { iRow, row ->
            row.mapIndexed { iCol, element ->
                if (element == 'S') Pair(iRow, iCol) else null
            }
        }.flatten().filterNotNull().first()
        val distances: List<List<Int>> = map.map { row -> row.map { -1 }}
        var currentDistance = 0
        while (true) {
            val next = Pair(current.first - 1, current.second)
            if (map[next.first][next.second] == '|') {
                current = next
                currentDistance += 1
                distances
            }
        }
        return -1
    }

    override fun solvePart2(): Long {
        return -1
    }
}