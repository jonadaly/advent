import re
from pathlib import Path

chunks = Path("10.txt").read_text().strip().split("\n")
syntax_error_score_chars = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}
autocomplete_score_chars = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4,
}


def simplify(_chunk):
    new_chunk = re.sub(r"(\(\)|\[]|{}|<>)", "", _chunk)
    if new_chunk == _chunk:
        return new_chunk
    return simplify(new_chunk)


autocomplete_scores = []
syntax_error_score = 0
for chunk in chunks:
    chunk = simplify(chunk)
    illegals = re.findall(
        r"\(]|\(}|\(>|\[\)|\[}|\[>|{\)|{]|{>|<\)|<]|<}",
        chunk,
    )
    if len(illegals) > 0:
        # Line is corrupt.
        syntax_error_score += syntax_error_score_chars[illegals[0][1]]
    else:
        # Line is incomplete.
        chunk_error_score = 0
        for c in chunk[::-1]:
            chunk_error_score = (chunk_error_score * 5) + autocomplete_score_chars[c]
        autocomplete_scores.append(chunk_error_score)

print(f"Part 1: syntax error score is {syntax_error_score}")
print(
    f"Part 1: autocomplete score is {sorted(autocomplete_scores)[int(len(autocomplete_scores)/2)]}"
)
