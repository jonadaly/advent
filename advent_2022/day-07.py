import itertools
from dataclasses import dataclass, field
from pathlib import Path

terminal: list[str] = Path("day-07-input.txt").read_text().strip().split("\n")


@dataclass
class Directory:
    parent: "Directory" | None
    path: Path
    children: list["Directory"] = field(default_factory=list)
    files: list[int] = field(default_factory=list)

    @property
    def size(self) -> int:
        return sum(child.size for child in self.children) + sum(self.files)

    @property
    def flat_list(self) -> list["Directory"]:
        return self.children + list(
            itertools.chain(*[c.flat_list for c in self.children])
        )


root_dir = Directory(parent=None, path=Path("/"))
current_dir = root_dir
for line in terminal[1:]:
    match line.split(" "):
        case ["$", "cd", ".."]:
            if current_dir.parent is None:
                break
            current_dir = current_dir.parent
        case ["$", "cd", newpath]:
            child = Directory(parent=current_dir, path=current_dir.path / newpath)
            current_dir.children.append(child)
            current_dir = child
        case ["$", "ls"]:
            continue
        case ["dir", _]:
            continue
        case [file_size, _]:
            current_dir.files.append(int(file_size))


total = sum(d.size for d in root_dir.flat_list if d.size <= 100_000)
print(f"Part 1: small dirs contain {total} bytes")

REQUIRED_DIR_SIZE = root_dir.size - 40_000_000
smallest = min(d.size for d in root_dir.flat_list if d.size >= REQUIRED_DIR_SIZE)
print(f"Part 2: smallest dir to delete has {smallest} bytes")
