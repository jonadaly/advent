import io.kotest.matchers.shouldBe
import org.junit.jupiter.api.Test

class Day7Test {
    private val day7 = Day7()
    private val testInput =
        """
        32T3K 765
        T55J5 684
        KK677 28
        KTJJT 220
        QQQJA 483
        """.trimIndent()

    @Test
    fun `part 1 should work for test input`() {
        day7.input = testInput
        day7.solvePart1() shouldBe 6440
    }

    @Test
    fun `part 2 should work for test input`() {
        day7.input = testInput
        day7.solvePart2() shouldBe 5905
    }
}
