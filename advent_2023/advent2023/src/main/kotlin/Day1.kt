fun main() {
    val day1 = Day1()
    println("Part 1: sum of calibration values is ${day1.solvePart1()}")
    println("Part 2: sum of calibration values is ${day1.solvePart2()}")
}

class Day1 : BaseDay("/input1.txt") {
    override fun solvePart1(): Int {
        return calibrate(input)
    }

    override fun solvePart2(): Int {
        return calibrate(replaceNumbers(input))
    }

    private fun calibrate(codes: String): Int {
        return codes.lines().sumOf { line ->
            line.filter { it.isDigit() }
                .let { digits -> digits.first().toString() + digits.last().toString() }
                .toInt()
        }
    }

    private fun replaceNumbers(input: String): String {
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
        return mappings.entries.fold(input) { acc, (key, value) -> acc.replace(key, value) }
    }
}
