import io.kotest.matchers.shouldBe
import org.junit.jupiter.api.Test

class Day9Test {
    private val day = Day9()
    private val testInput =
        """
        0 3 6 9 12 15
        1 3 6 10 15 21
        10 13 16 21 30 45
        """.trimIndent()

    @Test
    fun `part 1 should work for test input`() {
        day.input = testInput
        day.solvePart1() shouldBe 114
    }

    @Test
    fun `part 2 should work for test input`() {
        day.input = testInput
        day.solvePart2() shouldBe 2
    }
}
