import io.kotest.matchers.shouldBe
import org.junit.jupiter.api.Test

class Day8Test {
    private val day8 = Day8()

    @Test
    fun `part 1 should work for first test input`() {
        day8.input =
            """
            RL
            
            AAA = (BBB, CCC)
            BBB = (DDD, EEE)
            CCC = (ZZZ, GGG)
            DDD = (DDD, DDD)
            EEE = (EEE, EEE)
            GGG = (GGG, GGG)
            ZZZ = (ZZZ, ZZZ)
            """.trimIndent()
        day8.solvePart1() shouldBe 2
    }

    @Test
    fun `part 1 should work for second test input`() {
        day8.input =
            """
            LLR

            AAA = (BBB, BBB)
            BBB = (AAA, ZZZ)
            ZZZ = (ZZZ, ZZZ)
            """.trimIndent()
        day8.solvePart1() shouldBe 6
    }

    @Test
    fun `part 2 should work for test input`() {
        day8.input =
            """
            LR
            
            11A = (11B, XXX)
            11B = (XXX, 11Z)
            11Z = (11B, XXX)
            22A = (22B, XXX)
            22B = (22C, 22C)
            22C = (22Z, 22Z)
            22Z = (22B, 22B)
            XXX = (XXX, XXX)
            """.trimIndent()
        day8.solvePart2() shouldBe 6
    }
}
