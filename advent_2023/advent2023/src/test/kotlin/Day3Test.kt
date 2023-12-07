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
    private val day3 = Day3()

    @Test
    fun `part 1 should work for test input`() {
        day3.input = testInput
        day3.solvePart1() shouldBe 4361
    }

    @Test
    fun `part 2 should work for test input`() {
        day3.input = testInput
        day3.solvePart2() shouldBe 467835
    }
}
