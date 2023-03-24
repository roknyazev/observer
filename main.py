import dataclasses
from pathlib import *


def scanner(root: str, depth: int):
    level_patterns = [f'.{"/*" * i}' for i in range(1, depth + 1)]

    def _scan():
        result = []
        for level_index, level_pattern in enumerate(level_patterns):
            level = set()
            for path in Path(root).glob(level_pattern):
                (level_index == 0 or (path.parent in result[level_index - 1])) and level.add(path)
            result.append(level)
        return result

    return _scan


@dataclasses.dataclass
class ScanDiff:
    created: set[Path]
    deleted: set[Path]


def diff(prev_scan: list[set[Path]] | None, current_scan: list[set[Path]]):
    if prev_scan is None:
        prev_scan = [set()] * len(current_scan)
    return [ScanDiff(created=curr - prev,
                     deleted=prev - curr) for prev, curr in zip(prev_scan, current_scan)]


scan = scanner('./test', 5)
print(scan())
print(diff(scan(), scan()))
print(diff(None, scan()))

