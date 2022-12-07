from __future__ import annotations

from pathlib import Path


class File(object):
    def __init__(self, name: str, size: int) -> None:
        self.name = name
        self.size = size


class Directory(object):
    def __init__(
        self, parent: None | Directory = None, files: None | list[File] = None
    ) -> None:
        self.parent = parent
        self.files = files

    def addFile(self, file: File) -> None:
        if self.files is not None:
            self.files.append(file)
        else:
            self.files = [file]


def isFile(command: str) -> bool:
    return False


def performCommand(line: str, directory: Directory) -> None:
    pass


dataPath = Path(__file__).with_name("Data.txt")
with open(dataPath) as dataFile:
    baseDirectory = Directory()
    for line in dataFile:
        performCommand(line, baseDirectory)
