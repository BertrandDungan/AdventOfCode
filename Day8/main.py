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


def treeTallEnoughToSee(forest: list[Tree], searchTree: Tree) -> bool:

    westTrees = [
        forestTree
        for forestTree in forest
        if forestTree.y == searchTree.y
        and forestTree.x < searchTree.x
        and forestTree.height >= searchTree.height
    ]
    EastTrees = [
        forestTree
        for forestTree in forest
        if forestTree.y == searchTree.y
        and forestTree.x > searchTree.x
        and forestTree.height >= searchTree.height
    ]
    northTrees = [
        forestTree
        for forestTree in forest
        if forestTree.x == searchTree.x
        and forestTree.y > searchTree.y
        and forestTree.height >= searchTree.height
    ]
    southTrees = [
        forestTree
        for forestTree in forest
        if forestTree.x == searchTree.x
        and forestTree.y < searchTree.y
        and forestTree.height >= searchTree.height
    ]

    return (
        len(westTrees) < 1
        or len(EastTrees) < 1
        or len(northTrees) < 1
        or len(southTrees) < 1
    )


dataPath = Path(__file__).with_name("Data.txt")
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
