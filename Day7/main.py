from __future__ import annotations

from pathlib import Path
from re import findall, search

MAX_SIZE = 100000


class File(object):
    def __init__(self, name: str, size: int, itemIndex: int = 0) -> None:
        self.name = name
        self.size = size
        self.itemIndex = itemIndex

    def getSize(self) -> tuple[int, int]:
        return (self.size, 0)


class Directory(object):
    def __init__(
        self,
        name: str,
        parent: None | Directory = None,
        children: list[File | Directory] = [],
        itemIndex: int = 0,
    ) -> None:
        self.name = name
        self.parent = parent
        self.children = children
        self.itemIndex = itemIndex

    def addItem(self, item: File | Directory) -> None:
        self.children.append(item)

    def addFile(self, line: str) -> None:
        fileSize, fileName = findall(r"([0-9]+) (.+)$", line)[0]
        self.addItem(File(fileName, int(fileSize), len(self.children)))

    def addDirectory(self, line: str) -> None:
        directoryName = search(r"r ([a-z]+)$", line)
        assert directoryName is not None
        self.addItem(Directory(directoryName[1], self, [], len(self.children)))

    def getSize(self) -> tuple[int, int]:
        if self.children is None:
            return (0, 0)
        sizeAcc = 0
        directoryAcc = 0
        for item in self.children:
            itemSize = item.getSize()
            sizeAcc += itemSize[0]
            if isinstance(item, Directory):
                directoryAcc += itemSize[1]
                if itemSize[0] <= MAX_SIZE:
                    directoryAcc += itemSize[0]
        if sizeAcc > MAX_SIZE:
            sizeAcc = 0
        return (sizeAcc, directoryAcc)

    def goUpLevel(self) -> Directory:
        assert self.parent is not None
        assert self.parent.children is not None
        self.parent.children[self.itemIndex] = self
        return Directory(
            self.parent.name,
            self.parent.parent,
            self.parent.children,
            self.parent.itemIndex,
        )

    def changeDirectory(self, line: str) -> Directory:
        changeDirectoryDirection = search(r"cd ([a-z | .]+)$", line)
        assert changeDirectoryDirection is not None
        directoryIndex = findDirectoryIndex(
            changeDirectoryDirection[1], activeDirectory.children
        )
        newDirectory = self.children[directoryIndex]
        assert isinstance(newDirectory, Directory)
        return Directory(newDirectory.name, self, newDirectory.children, directoryIndex)


def isFile(line: str) -> bool:
    return line[0].isdigit()


def isDirectory(line: str) -> bool:
    return line[0] == "d"


def isDirectoryChange(line: str) -> bool:
    match = search(r"\$ cd [^/]", line)
    return match is not None


def findDirectoryIndex(directoryName: str, items: list[File | Directory]) -> int:
    for index, item in enumerate(items):
        if isinstance(item, Directory):
            if item.name == directoryName:
                return index
    raise Exception(f"No directory matching {directoryName} found")


def changeDirectory(line: str, activeDirectory: Directory) -> Directory:
    assert activeDirectory.children is not None
    changeDirectoryDirection = search(r"cd ([a-z | .]+)$", line)
    assert changeDirectoryDirection is not None
    if "." in changeDirectoryDirection[0]:
        return activeDirectory.goUpLevel()
    return activeDirectory.changeDirectory(line)


def performTerminalAction(line: str, activeDirectory: Directory) -> Directory:
    if isFile(line):
        activeDirectory.addFile(line)
    elif isDirectory(line):
        activeDirectory.addDirectory(line)
    elif isDirectoryChange(line):
        return changeDirectory(line, activeDirectory)
    return activeDirectory


def returnDirectoryToRoot(activeDirectory: Directory) -> Directory:
    rootDirectory = activeDirectory
    while rootDirectory.parent is not None:
        rootDirectory = rootDirectory.goUpLevel()
    assert rootDirectory is not None
    return rootDirectory


dataPath = Path(__file__).with_name("Test.txt")
with open(dataPath) as dataFile:
    activeDirectory = Directory("/")
    for line in dataFile:
        activeDirectory = performTerminalAction(line, activeDirectory)
    activeDirectory = returnDirectoryToRoot(activeDirectory)
    print(activeDirectory.getSize())
