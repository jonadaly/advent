import io.kotest.matchers.shouldBe
import org.junit.jupiter.api.Test

class Day10Test {
    private val day = Day10()
    private val testInput =
        """
        7-F7-
        .FJ|7
        SJLL7
        |F--J
        LJ.LJ
        """.trimIndent()

    @Test
    fun `part 1 should work for test input`() {
        day.input = testInput
        day.solvePart1() shouldBe -2
    }

    @Test
    fun `part 2 should work for test input`() {
        day.input = testInput
        day.solvePart2() shouldBe -2
    }
}