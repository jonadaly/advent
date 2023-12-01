fun main() {
    val realInput = object {}.javaClass.getResource("/input1.txt")!!.readText()
    val part1 = calibrate(realInput)
    val part2 = calibrate(replace(realInput))
    println("Part 1: sum of calibration values is $part1")
    println("Part 2: sum of calibration values is $part2")
}

fun calibrate(input: String): Int {
    return input.lines().sumOf { line ->
        line.filter { it.isDigit() }
            .let { digits -> digits.first().toString() + digits.last().toString() }
            .toInt()
    }
}

fun replace(input: String): String {
    val mappings =
        mapOf(
            "one" to "o1ne",
            "two" to "t2wo",
            "three" to "t3hree",
            "four" to "f4our",
            "five" to "f5ive",
            "six" to "s6ix",
            "seven" to "s7even",
            "eight" to "e8ight",
            "nine" to "n9ine",
            "zero" to "z0ero",
        )
    var replaced = input
    mappings.forEach { (key, value) -> replaced = replaced.replace(key, value) }
    return replaced
}
