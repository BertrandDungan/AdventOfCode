from __future__ import annotations

File = str


class Directory(object):
    def __init__(self, parent: None | Directory, children: None | list[File]) -> None:
        self.parent = parent
        self.children = children
