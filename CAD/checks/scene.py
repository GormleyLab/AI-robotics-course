"""Tree-position refs (``#o1.12.9``) into a STEP file, over cadgen 0.8's ``read_step``.

cadgen 0.7's ``read_scene`` addressed occurrences by their position in the
STEP tree; 0.8 dropped it. The Fusion map and the issue log name parts that
way, so the checks keep the scheme: ``o1`` is the STEP's root assembly and
``o1.N`` its Nth child, counted from 1, as 0.7 numbered them.

    scene = read_scene("STEP/imported/fusion/Joint 1 and 2.step")
    (ring,) = scene.resolve("#o1.12.9")
    ring.shape()          # the part placed in the assembly (world frame)
    for leaf in scene.leaves(): ...

``shape()`` carries the whole placement in its ``location``, so
``s.moved(s.location.inverse())`` gives the part in its own frame.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import build123d as bd
from cadgen import read_step


@dataclass
class Occurrence:
    ref: str
    label: str
    node: bd.Shape
    world: bd.Location
    children: list[Occurrence] = field(default_factory=list)
    kind: str = "occurrence"
    prototype_id: str = ""  # the same for every occurrence of one shared part

    def shape(self) -> bd.Shape:
        return self.node.located(self.world)


class Scene:
    def __init__(self, path: str):
        self.path = path
        root = read_step(path)
        self.roots = [self._walk(root, bd.Location(), "o1")]
        protos: list[Occurrence] = []
        for leaf in self.leaves():
            same = next((p for p in protos if p.node.wrapped.IsPartner(leaf.node.wrapped)), None)
            if same is None:
                protos.append(leaf)
                leaf.prototype_id = f"p{len(protos)}"
            else:
                leaf.prototype_id = same.prototype_id

    def _walk(self, node, holder, ref) -> Occurrence:
        here = holder * node.location
        occ = Occurrence(f"{self.path}#{ref}", node.label or "", node, here)
        occ.children = [self._walk(c, here, f"{ref}.{i}") for i, c in enumerate(node.children or (), 1)]
        return occ

    def _all(self):
        stack = list(reversed(self.roots))
        while stack:
            occ = stack.pop()
            yield occ
            stack.extend(reversed(occ.children))

    def leaves(self) -> list[Occurrence]:
        return [o for o in self._all() if not o.children]

    def resolve(self, ref: str) -> list[Occurrence]:
        """The occurrence a ``#o1.2.3`` ref names (optionally prefixed by the file's path)."""
        want = ref.rsplit("#", 1)[-1]
        found = [o for o in self._all() if o.ref.rsplit("#", 1)[-1] == want]
        if not found:
            raise KeyError(f"{self.path} has no occurrence {want}")
        return found


def read_scene(path: str) -> Scene:
    return Scene(str(path))
