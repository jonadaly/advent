import io.kotest.matchers.shouldBe
import org.junit.jupiter.api.Test

class Day6Test {
    private val day6 = Day6()
    private val testInput =
        """
        Time:      7  15   30
        Distance:  9  40  200
        """.trimIndent()

    @Test
    fun `part 1 should work for test input`() {
        day6.input = testInput
        day6.solvePart1() shouldBe 288
    }

    @Test
    fun `part 2 should work for test input`() {
        day6.input = testInput
        day6.solvePart2() shouldBe 71503
    }
}
