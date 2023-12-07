fun main() {
    val day6 = Day6()
    println("Part 1: Product of record count is ${day6.solvePart1()}")
    println("Part 2: Product of record count is ${day6.solvePart2()}")
}

class Day6 : BaseDay("/input6.txt") {
    override fun solvePart1(): Int {
        return findRecordProduct(parseDay6InputPart1(input))
    }

    override fun solvePart2(): Int {
        return findRecordProduct(parseDay6InputPart2(input))
    }

    private fun parseDay6InputPart1(input: String): Map<Long, Long> {
        // Convert input into a map of duration to record (time to distance).
        return input.lines()
            .map { line ->
                line.split("\\s+".toRegex())
                    .drop(1) // ignore first column
                    .map { it.toLong() }
            }
            .let { it[0].zip(it[1]).toMap() }
    }

    private fun parseDay6InputPart2(input: String): Map<Long, Long> {
        return input.lines()
            .map {
                it.split("\\s+".toRegex())
                    .drop(1) // ignore first column
                    .joinToString("")
                    .toLong()
            }
            .let { mapOf(it[0] to it[1]) }
    }

    private fun findRecordProduct(courses: Map<Long, Long>): Int {
        // Formula for distance after pushing for time t is d = t * (duration - t). Calculate all distances, then
        // count the number of distances that are greater than the record. Then take the product to get the answer.
        return courses.entries
            .map { (duration, record) ->
                (0..duration).map { it * (duration - it) }.filter { it > record }.size
            }.reduce(Int::times)
    }
}
