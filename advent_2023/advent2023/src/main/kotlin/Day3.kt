

fun main() {
    val day = Day3()
    println("Part 1: Sum of part numbers is ${day.solvePart1()}")
    println("Part 2: Sum of gear ratios is ${day.solvePart2()}")
}

class Day3 : BaseDay("/input3.txt") {
    data class PartNumber(var value: Int, val iRow: Int, val iColStart: Int, var iColEnd: Int) {
        fun isAdjacentTo(coordinates: Pair<Int, Int>): Boolean {
            return (
                coordinates.first in (this.iRow - 1)..(this.iRow + 1) &&
                    coordinates.second in (this.iColStart - 1)..(this.iColEnd + 1)
            )
        }
    }

    override fun solvePart1(): Int {
        val grid = parseInput(input)
        val symbolCoordinates = findSymbolCoordinates(grid, "*+&=$@/-%#")
        val numberCoordinates = findNumberCoordinates(grid)
        return numberCoordinates.filter { number ->
            symbolCoordinates.any { number.isAdjacentTo(it) }
        }.sumOf { it.value }
    }

    override fun solvePart2(): Int {
        val grid = parseInput(input)
        val symbolCoordinates = findSymbolCoordinates(grid, "*")
        val numberCoordinates = findNumberCoordinates(grid)
        return symbolCoordinates.sumOf {
            numberCoordinates.filter { part: PartNumber -> part.isAdjacentTo(it) }.let { numbers ->
                // Include only gears with exactly two neighbouring part numbers.
                if (numbers.size == 2) numbers[0].value * numbers[1].value else 0
            }
        }
    }

    private fun parseInput(input: String): List<CharArray> {
        return input.lines().map { it.toCharArray() }
    }

    private fun findSymbolCoordinates(
        grid: List<CharArray>,
        symbols: String,
    ) = grid.mapIndexed { iRow, row ->
        row.mapIndexed { iCol, element ->
            if (symbols.contains(element)) Pair(iRow, iCol) else null
        }
    }.flatten().filterNotNull()

    private fun findNumberCoordinates(grid: List<CharArray>): List<PartNumber> {
        // Find coordinates of contiguous groups of numbers, which can be multiple digits.
        return grid.flatMapIndexed { iRow, row ->
            "\\d+".toRegex().findAll(row.joinToString("")).map {
                PartNumber(it.value.toInt(), iRow, it.range.first, it.range.last)
            }
        }
    }
}
