import io.kotest.matchers.shouldBe
import org.junit.jupiter.api.Test

class Day3Test {
    private val testInput =
        """
        467..114..
        ...*......
        ..35..633.
        ......#...
        617*......
        .....+.589
        ..592.....
        ......755.
        ...$.*....
        .664.598..
        """.trimIndent()
    private val day = Day3()

    @Test
    fun `part 1 should work for test input`() {
        day.input = testInput
        day.solvePart1() shouldBe 4361
    }

    @Test
    fun `part 2 should work for test input`() {
        day.input = testInput
        day.solvePart2() shouldBe 467835
    }
}
