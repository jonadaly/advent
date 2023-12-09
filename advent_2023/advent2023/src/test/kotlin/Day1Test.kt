import io.kotest.matchers.shouldBe
import org.junit.jupiter.api.Test

class Day1Test {
    private val day = Day1()

    @Test
    fun `part 1 should work for test input`() {
        day.input =
            """
            1abc2
            pqr3stu8vwx
            a1b2c3d4e5f
            treb7uchet
            """.trimIndent()
        day.solvePart1() shouldBe 142
    }

    @Test
    fun `part2 should work for test input`() {
        day.input =
            """
            two1nine
            eightwothree
            abcone2threexyz
            xtwone3four
            4nineeightseven2
            zoneight234
            7pqrstsixteen
            """.trimIndent()
        day.solvePart2() shouldBe 281
    }
}
