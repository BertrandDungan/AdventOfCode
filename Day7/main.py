from __future__ import annotations

from pathlib import Path
from re import Match, findall, search
from typing import Optional

STEP_ONE_SEARCH_SIZE = 100000
TOTAL_DISK_SPACE = 70_000_000
UPDATE_SIZE = 3_000_0000


class File(object):
    def __init__(self, name: str, size: int, itemIndex: int = 0) -> None:
        self.name = name
        self.size = size
        self.itemIndex = itemIndex

    def getSize(self, _: int) -> tuple[int, int]:
        return (self.size, 0)


class Directory(object):
    def __init__(
        self,
        name: str,
        parent: Optional[Directory] = None,
        children: list[File | Directory] = [],
        itemIndex: int = 0,
    ) -> None:
        self.name = name
        self.parent = parent
        self.children = children
        self.itemIndex = itemIndex

    def addItem(self, item: File | Directory) -> None:
        self.children.append(item)

    def addFile(self, line: str) -> Directory:
        fileSize, fileName = findall(r"([0-9]+) (.+)$", line)[0]
        self.addItem(File(fileName, int(fileSize), len(self.children)))
        return self

    def addDirectory(self, line: str) -> Directory:
        directoryName = search(r"r ([a-z]+)$", line)
        assert directoryName is not None
        self.addItem(Directory(directoryName[1], self, [], len(self.children)))
        return self

    def getSize(self, maxSize: int) -> tuple[int, int]:
        if self.children is None:
            return (0, 0)
        selfSizeAcc = 0
        directoryAcc = 0
        for item in self.children:
            itemSize = item.getSize(maxSize)
            selfSizeAcc += itemSize[0]
            directoryAcc += itemSize[1]
        if selfSizeAcc <= maxSize:
            directoryAcc += selfSizeAcc

        return (selfSizeAcc, directoryAcc)

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

    def changeDirectory(self, direction: Match[str]) -> Directory:
        directoryIndex = findDirectoryIndex(direction[1], activeDirectory.children)
        newDirectory = self.children[directoryIndex]
        assert isinstance(newDirectory, Directory)
        return Directory(newDirectory.name, self, newDirectory.children, directoryIndex)

    def getSmallestDirectoryOfSize(self, searchSize: int) -> int:
        smallestDirectory = self.getSize(TOTAL_DISK_SPACE)[0]
        for item in self.children:
            if isinstance(item, Directory):
                itemSize = item.getSmallestDirectoryOfSize(searchSize)
                if itemSize < smallestDirectory and itemSize >= searchSize:
                    smallestDirectory = itemSize
        return smallestDirectory


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
    raise Exception(f"No directory found matching {directoryName}")


def changeDirectory(line: str, activeDirectory: Directory) -> Directory:
    assert activeDirectory.children is not None
    changeDirectoryDirection = search(r"cd ([a-z | .]+)$", line)
    assert changeDirectoryDirection is not None
    if "." in changeDirectoryDirection[0]:
        return activeDirectory.goUpLevel()
    return activeDirectory.changeDirectory(changeDirectoryDirection)


def performTerminalAction(line: str, activeDirectory: Directory) -> Directory:
    if isFile(line):
        return activeDirectory.addFile(line)
    elif isDirectory(line):
        return activeDirectory.addDirectory(line)
    elif isDirectoryChange(line):
        return changeDirectory(line, activeDirectory)
    return activeDirectory


def returnDirectoryToRoot(activeDirectory: Directory) -> Directory:
    rootDirectory = activeDirectory
    while rootDirectory.parent is not None:
        rootDirectory = rootDirectory.goUpLevel()
    assert rootDirectory is not None
    return rootDirectory


dataPath = Path(__file__).with_name("Data.txt")
with open(dataPath) as dataFile:
    activeDirectory = Directory("/")
    for line in dataFile:
        activeDirectory = performTerminalAction(line, activeDirectory)
    activeDirectory = returnDirectoryToRoot(activeDirectory)
    size = activeDirectory.getSize(STEP_ONE_SEARCH_SIZE)
    print(
        f"Total size of directories smaller than {STEP_ONE_SEARCH_SIZE + 1} "
        + f"is {size[1]}"
    )
    print(f"Total space used: {size[0]}")
    print(f"Total free space is: {TOTAL_DISK_SPACE-size[0]}")
    spaceNeededForUpdate = UPDATE_SIZE - (TOTAL_DISK_SPACE - size[0])
    print(f"You need to free up {spaceNeededForUpdate} space to perform the update")
    smallestDirectoryToDelete = activeDirectory.getSmallestDirectoryOfSize(
        spaceNeededForUpdate
    )
    print(
        f"You can delete a directory of size {smallestDirectoryToDelete}"
        + "to perform this update"
    )
