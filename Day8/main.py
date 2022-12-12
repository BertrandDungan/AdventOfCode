from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Tree:
    height: int
    x: int
    y: int


def makeTree(treeHeight: str, xPosition: int, yPosition: int) -> Tree:
    return Tree(int(treeHeight), xPosition, yPosition)


def treeOnForestEdge(tree: Tree) -> bool:
    return tree.x == 0 or tree.x == forestMaxX or tree.y == 0 or tree.y == forestMaxY


def treeTallEnoughToSee(forest: list[Tree], tree: Tree) -> bool:
    return False


dataPath = Path(__file__).with_name("Test.txt")
with open(dataPath) as dataFile:
    forest: list[Tree] = []
    forestMaxY = 0
    forestMaxX = 0
    forestLines = enumerate(dataFile)
    for yIndex, line in forestLines:
        for xIndex, treeChar in enumerate(line):
            if treeChar != "\n":
                forest.append(makeTree(treeChar, xIndex, yIndex))
                forestMaxX = xIndex
        forestMaxY = yIndex
    treesVisibleFromOutside = 0
    for tree in forest:
        if treeOnForestEdge(tree):
            treesVisibleFromOutside += 1
        elif treeTallEnoughToSee(forest, tree):
            treesVisibleFromOutside += 1
    print(treesVisibleFromOutside)
