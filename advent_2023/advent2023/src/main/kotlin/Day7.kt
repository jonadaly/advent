

fun main() {
    val day7 = Day7()
    println("Part 1: winnings total is ${day7.solvePart1()}")
    println("Part 2: winnings total is ${day7.solvePart2()}")
}

class Day7: BaseDay("/input7.txt") {

    private enum class HandType(val value: Int) {
        FIVE_OF_A_KIND(7),
        FOUR_OF_A_KIND(6),
        FULL_HOUSE(5),
        THREE_OF_A_KIND(4),
        TWO_PAIR(3),
        ONE_PAIR(2),
        HIGH_CARD(1),
    }

    override fun solvePart1(): Int {
        return calculateWinnings(parseDay7Input(input), jacksWild = false)
    }

    override fun solvePart2(): Int {
        return calculateWinnings(parseDay7Input(input), jacksWild = true)
    }


    private fun parseDay7Input(input: String): Map<String, Int> {
        return input.lines().map { it.split(" ") }.associate { it[0] to it[1].toInt() }
    }

    private fun calculateWinnings(
        handMap: Map<String, Int>,
        jacksWild: Boolean,
    ): Int {
        val handRanks =
            handMap.toSortedMap(compareBy<String> { getHandType(it, jacksWild) }.thenBy { getHandOrder(it, jacksWild) })
        return handRanks.entries.mapIndexed { ind, (_, bid) ->
            bid * (ind + 1)
        }.sum()
    }



    private fun getHandType(
        hand: String,
        jacksWild: Boolean,
    ): Int {
        val numWilds = if (jacksWild) hand.count { it == 'J' } else 0
        val cardCount =
            hand.groupingBy { it }.eachCount().mapValues { if (it.key == 'J') it.value - numWilds else it.value }
                .filter { it.value > 0 }
        val maxCount = cardCount.values.maxOrNull() ?: 0
        if (maxCount + numWilds == 5) return HandType.FIVE_OF_A_KIND.value
        if (maxCount + numWilds == 4) return HandType.FOUR_OF_A_KIND.value
        if (maxCount + numWilds == 3) {
            return if (cardCount.size == 2) HandType.FULL_HOUSE.value else HandType.THREE_OF_A_KIND.value
        }
        if (maxCount + numWilds == 2) {
            return if (hand.chars().distinct().count() == 3L) HandType.TWO_PAIR.value else HandType.ONE_PAIR.value
        }
        return HandType.HIGH_CARD.value
    }

    private fun getHandOrder(
        hand: String,
        jacksWild: Boolean,
    ): Int {
        return Integer.parseInt(
            hand.replace("T", "a")
                .replace("J", if (jacksWild) "0" else "b")
                .replace("Q", "c")
                .replace("K", "d")
                .replace("A", "e"),
            16,
        )
    }
}