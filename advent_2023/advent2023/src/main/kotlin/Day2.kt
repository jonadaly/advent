fun main() {
    val day2 = Day2()
    println("Part 1: Sum of indexes of possible games is ${day2.solvePart1()}")
    println("Part 2: Sum of cube power is ${day2.solvePart2()}")
}

class Day2 : BaseDay("/input2.txt") {
    override fun solvePart1(): Int {
        return getPossibleIndexSum(parseDay2Input(input))
    }

    override fun solvePart2(): Int {
        return getPowerSum(parseDay2Input(input))
    }

    private fun parseDay2Input(input: String): List<List<Triple<Int, Int, Int>>> {
        return input.lines()
            .map { line ->
                line.split(":")[1].trim().split(";").map {
                    Triple(
                        "(\\d+) red".toRegex().find(it)?.groupValues?.get(1)?.toInt() ?: 0,
                        "(\\d+) green".toRegex().find(it)?.groupValues?.get(1)?.toInt() ?: 0,
                        "(\\d+) blue".toRegex().find(it)?.groupValues?.get(1)?.toInt() ?: 0,
                    )
                }
            }
    }

    private fun getPossibleIndexSum(games: List<List<Triple<Int, Int, Int>>>): Int {
        return games
            .map { game ->
                game.all { round ->
                    round.first <= 12 && round.second <= 13 && round.third <= 14
                }
            }
            .mapIndexed { ind, poss -> if (poss) ind + 1 else 0 }.sum()
    }

    private fun getPowerSum(games: List<List<Triple<Int, Int, Int>>>): Int {
        // Can make this more efficient by only iterating through the rounds once, but this is easier to read.
        return games.sumOf { game ->
            game.maxOf { it.first } * game.maxOf { it.second } * game.maxOf { it.third }
        }
    }
}
