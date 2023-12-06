import io.kotest.matchers.shouldBe
import org.junit.jupiter.api.Test

class Day6Test {
    private val testInput =
        """
        Time:      7  15   30
        Distance:  9  40  200
        """.trimIndent()

    @Test
    fun `part 1 should work for test input`() {
        val courses = parseInputPart1(testInput)
        findRecordProduct(courses) shouldBe 288
    }

    @Test
    fun `part 2 should work for test input`() {
        val courses = parseInputPart2(testInput)
        findRecordProduct(courses) shouldBe 71503
    }
}
