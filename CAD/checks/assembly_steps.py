"""Check an assembly-guide chapter's step list against its assembly and the print list.

    cd CAD
    PYTHONPATH=src ~/.local/bin/cadgen +0.8.2 run checks/assembly_steps.py gearbox

- every part in the assembly STEP is added by exactly one numbered step, and no
  step names a part the assembly does not have;
- no picture draws a part as already installed before an earlier picture or step adds it
  (a part can appear in colour earlier, as the ring gear does while it takes its inserts);
- each printed model's count in the assembly equals its count in tools/print_parts.py;
- the bought-part counts equal design.md's parts table;
- every picture exists, and every picture the guide links does too.
"""
from __future__ import annotations

import ast
import importlib
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for extra in (ROOT, ROOT / "tools"):
    if str(extra) not in sys.path:
        sys.path.insert(0, str(extra))

from checks.scene import read_scene

# Assembly model -> its row in design.md's parts table.
BOUGHT = {"gearbox": {"planet_pin": "Pin 6x11mm", "bushing": "Bushing 8mm", "washer": "Washer 6mm"}}


def printed_counts() -> dict[str, int]:
    """PRINTED in tools/print_parts.py, read and not imported: importing it sets fit profiles."""
    source = (ROOT / "tools" / "print_parts.py").read_text(encoding="utf-8")
    table = next(n.value for n in ast.parse(source).body
                 if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "PRINTED")
    return {name: count for name, (_, count) in ast.literal_eval(table).items()}


def main(name: str) -> int:
    chapter = importlib.import_module(f"assembly_steps.{name}")
    labels = [leaf.label for leaf in read_scene(str(ROOT / chapter.ASSEMBLY)).leaves()]
    problems: list[str] = []

    numbered = [s for s in chapter.STEPS if s.number.isdigit()]
    adds = Counter(label for s in numbered for label in s.adds)
    problems += [f"added {n} times: {label}" for label, n in adds.items() if n != 1]
    problems += [f"never added: {label}" for label in labels if label not in adds]
    problems += [f"not in the assembly: {label}" for label in adds if label not in labels]

    installed: set[str] = set()
    for step in numbered:
        for view in step.views:
            for label in view.built:
                if label not in installed:
                    problems.append(f"{view.name} shows {label} as installed before it has been added")
            installed |= set(view.added)
        installed |= set(step.adds)

    printed = printed_counts()
    models = Counter(label.split(":")[0] for label in labels)
    in_print_list = {m: n for m, n in models.items() if m in printed}
    problems += [f"{m}: {n} in the assembly, {printed[m]} in print_parts.py"
                 for m, n in in_print_list.items() if printed[m] != n]

    design = (ROOT / "docs" / "design.md").read_text(encoding="utf-8")
    for model, row in BOUGHT.get(name, {}).items():
        match = re.search(rf"^\|\s*`{re.escape(row)}`\s*\|\s*(\d+)\s*\|", design, re.M)
        if not match:
            problems.append(f"design.md has no row for {row}")
        elif int(match.group(1)) != models[model]:
            problems.append(f"{model}: {models[model]} in the assembly, {match.group(1)} in design.md")

    img = ROOT / "docs" / "img"
    for step in chapter.STEPS:
        for view in step.views:
            path = img / view.path if view.path else img / "assembly" / chapter.NAME / f"{view.name}.png"
            if not path.exists():
                problems.append(f"missing picture: {path.relative_to(ROOT)}")
    guide = ROOT / "docs" / "assembly-guide.md"
    if guide.exists():
        for link in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", guide.read_text(encoding="utf-8")):
            if not (guide.parent / link).exists():
                problems.append(f"the guide links a missing picture: {link}")

    print(f"{name}: {len(labels)} parts, {sum(adds.values())} added across {len(numbered)} steps; "
          f"printed: {sum(in_print_list.values())} parts of {len(in_print_list)} models")
    for problem in problems:
        print("FAIL", problem)
    print("FAIL" if problems else "PASS")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "gearbox"))
