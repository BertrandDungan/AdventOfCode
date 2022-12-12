from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Tree:
    height: int
    x: int
    y: int


def makeTree(treeHeight: str, xPosition: int, yPosition: int) -> Tree:
    return Tree(int(treeHeight), xPosition, yPosition)


def treeOnForestEdge(xIndex: int, yIndex: int, forestMaxX, forestMaxY) -> bool:
    return xIndex == 0 or yIndex == forestMaxX or tree.y == 0 or tree.y == forestMaxY


def getTreesInView(forest: list[Tree], searchTree: Tree) -> list[list[Tree]]:
    return [
        [
            forestTree
            for forestTree in forest
            if forestTree.y == searchTree.y
            and forestTree.x < searchTree.x
            and forestTree.height >= searchTree.height
        ],
        [
            forestTree
            for forestTree in forest
            if forestTree.y == searchTree.y
            and forestTree.x > searchTree.x
            and forestTree.height >= searchTree.height
        ],
        [
            forestTree
            for forestTree in forest
            if forestTree.x == searchTree.x
            and forestTree.y > searchTree.y
            and forestTree.height >= searchTree.height
        ],
        [
            forestTree
            for forestTree in forest
            if forestTree.x == searchTree.x
            and forestTree.y < searchTree.y
            and forestTree.height >= searchTree.height
        ],
    ]


def treeTallEnoughToSee(forest, tree, xIndex, yIndex, forestMaxX, forestMaxY) -> bool:
    # for xIndex in range(xIndex, forestMaxX):
    return False
    # return any(len(tree) < 1 for tree in treesInView)


def getTreeScore(
    blockingTrees: list[list[Tree]], treeToScore: Tree, maxY: int, maxX: int
) -> int:
    return 0


dataPath = Path(__file__).with_name("Test.txt")
with open(dataPath) as dataFile:
    forestLines = enumerate(dataFile)
    forest = []
    forestMaxX = 0
    forestMaxY = 0
    for yIndex, line in forestLines:
        forest.append([])
        for xIndex, treeChar in enumerate(line):
            if treeChar != "\n":
                currentTreeLine = forest[yIndex]
                assert isinstance(currentTreeLine, list)
                currentTreeLine.append(int(treeChar))
                forestMaxX = xIndex
        forestMaxY = yIndex
    treesVisibleFromOutside = 0
    bestTreeScore = 0
    for xIndex, treeLine in enumerate(forest):
        for yIndex, tree in enumerate(treeLine):
            if treeOnForestEdge(xIndex, yIndex, forestMaxX, forestMaxY):
                treesVisibleFromOutside += 1
            elif treeTallEnoughToSee(
                forest, tree, xIndex, yIndex, forestMaxX, forestMaxY
            ):
                treesVisibleFromOutside += 1
            # treeScore = getTreeScore(blockingTrees, tree, forestMaxY, forestMaxX)
            # if treeScore > bestTreeScore:
            #     bestTreeScore = treeScore
            # bestTree = tree

    print(f"You can see {treesVisibleFromOutside} trees from outside")
    print(f"The best tree score is: {bestTreeScore}")
