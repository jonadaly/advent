abstract class BaseDay(fileName: String) {
    var input: String = object {}.javaClass.getResource(fileName)!!.readText().trim()

    abstract fun solvePart1(): Any

    abstract fun solvePart2(): Any
}
