import io.kotest.matchers.shouldBe
import org.junit.jupiter.api.Test

class Day5Test {
    private val day = Day5()
    private val testInput =
        """
        seeds: 79 14 55 13

        seed-to-soil map:
        50 98 2
        52 50 48

        soil-to-fertilizer map:
        0 15 37
        37 52 2
        39 0 15

        fertilizer-to-water map:
        49 53 8
        0 11 42
        42 0 7
        57 7 4

        water-to-light map:
        88 18 7
        18 25 70

        light-to-temperature map:
        45 77 23
        81 45 19
        68 64 13

        temperature-to-humidity map:
        0 69 1
        1 0 69

        humidity-to-location map:
        60 56 37
        56 93 4
        """.trimIndent()

    @Test
    fun `part 1 should work for test input`() {
        day.input = testInput
        day.solvePart1() shouldBe 35
    }

    @Test
    fun `part 2 should work for test input`() {
        day.input = testInput
        day.solvePart2() shouldBe 46
    }
}