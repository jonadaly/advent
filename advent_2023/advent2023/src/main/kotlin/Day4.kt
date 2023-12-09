import kotlin.math.pow

fun main() {
    val day = Day4()
    println("Part 1: Total points is ${day.solvePart1()}")
    println("Part 2: Total scratchcards won is ${day.solvePart2()}")
}

class Day4 : BaseDay("/input4.txt") {
    data class Card(val id: Int, val winningNumbers: Set<Int>, val myNumbers: Set<Int>)

    override fun solvePart1(): Int {
        val cards = parseInput(input)
        return cards.map { countWinningNumbers(it) }.sumOf { if (it == 0) 0.0 else 2.0.pow(it - 1) }.toInt()
    }

    override fun solvePart2(): Int {
        val cards = parseInput(input)
        val holdings: MutableMap<Int, Int> = cards.associate { it.id to 1 }.toMutableMap()
        for (card in cards) {
            val copies = holdings[card.id]!!
            val matches = card.myNumbers.intersect(card.winningNumbers).size
            for (i in 1..matches) {
                holdings[card.id + i] = holdings[card.id + i]!!.plus(copies)
            }
        }
        return holdings.values.sum()
    }

    private fun countWinningNumbers(card: Card): Int {
        return card.myNumbers.intersect(card.winningNumbers).size
    }

    private fun parseInput(input: String): List<Card> {
        return input.lines().map { line -> line.split(":")[1] }.mapIndexed { idx, line ->
            val parts = line.split("|")
            Card(
                id = idx + 1,
                winningNumbers = parts[0].trim().split("\\s+".toRegex()).map { it.toInt() }.toSet(),
                myNumbers = parts[1].trim().split("\\s+".toRegex()).map { it.toInt() }.toSet(),
            )
        }
    }
}
