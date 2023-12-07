fun main() {
    val realInput = object {}.javaClass.getResource("/input6.txt")!!.readText()

    // Convert input into a map of duration to record (time to distance).
    val coursesPart1 = parseDay6InputPart1(realInput)
    val coursesPart2 = parseDay6InputPart2(realInput)

    println("Part 1: Product of record count is ${findRecordProduct(coursesPart1)}")
    println("Part 2: Product of record count is ${findRecordProduct(coursesPart2)}")
}

fun parseDay6InputPart1(input: String): Map<Long, Long> {
    return input.lines()
        .map { line ->
            line.split("\\s+".toRegex())
                .drop(1) // ignore first column
                .map { it.toLong() }
        }
        .let { it[0].zip(it[1]).toMap() }
}

fun parseDay6InputPart2(input: String): Map<Long, Long> {
    return input.lines()
        .map {
            it.split("\\s+".toRegex())
                .drop(1) // ignore first column
                .joinToString("")
                .toLong()
        }
        .let { mapOf(it[0] to it[1]) }
}

fun findRecordProduct(courses: Map<Long, Long>): Int {
    // Formula for distance after pushing for time t is d = t * (duration - t). Calculate all distances, then
    // count the number of distances that are greater than the record. Then take the product to get the answer.
    return courses.entries
        .map { (duration, record) ->
            (0..duration).map { it * (duration - it) }.filter { it > record }.size
        }.reduce(Int::times)
}
