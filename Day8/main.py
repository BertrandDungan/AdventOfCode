from pathlib import Path


def treeOnForestEdge(
    xIndex: int, yIndex: int, forestMaxX: int, forestMaxY: int
) -> bool:
    return xIndex == 0 or yIndex == 0 or xIndex == forestMaxX or yIndex == forestMaxY


def westViewLen(
    forest: list[list[int]], xIndex: int, yIndex: int, treeHeight: int
) -> int:
    lowerTrees = 0
    for tree in reversed(forest[yIndex][0:xIndex]):
        if tree < treeHeight:
            lowerTrees += 1
        else:
            return lowerTrees
    return lowerTrees


def eastViewLen(
    forest: list[list[int]], xIndex: int, yIndex: int, treeHeight: int, forestMaxX: int
) -> int:
    lowerTrees = 0
    for tree in forest[yIndex][xIndex + 1 : forestMaxX + 1]:
        if tree < treeHeight:
            lowerTrees += 1
        else:
            return lowerTrees
    return lowerTrees


def northViewLen(
    forest: list[list[int]], xIndex: int, yIndex: int, treeHeight: int
) -> int:
    lowerTrees = 0
    for tree in reversed([tree[xIndex] for tree in forest[0:yIndex]]):
        if tree < treeHeight:
            lowerTrees += 1
        else:
            return lowerTrees
    return lowerTrees


def southViewLen(
    forest: list[list[int]], xIndex: int, yIndex: int, treeHeight: int, forestMaxY: int
) -> int:
    lowerTrees = 0
    for tree in forest[yIndex + 1 : forestMaxY + 1]:
        if tree[xIndex] < treeHeight:
            lowerTrees += 1
        else:
            return lowerTrees
    return lowerTrees


def treeTallEnoughToSee(
    forest: list[list[int]],
    treeHeight: int,
    xIndex: int,
    yIndex: int,
    forestMaxX: int,
    forestMaxY: int,
) -> bool:
    westView = westViewLen(forest, xIndex, yIndex, treeHeight)
    if westView == xIndex:
        return True
    eastView = eastViewLen(forest, xIndex, yIndex, treeHeight, forestMaxX)
    if eastView == forestMaxX - xIndex:
        return True
    northView = northViewLen(forest, xIndex, yIndex, treeHeight)
    if northView == yIndex:
        return True
    southView = southViewLen(forest, xIndex, yIndex, treeHeight, forestMaxY)
    if southView == forestMaxY - yIndex:
        return True
    return False


def getTreeScore(
    forest: list[list[int]],
    xIndex: int,
    yIndex: int,
    treeHeight: int,
    forestMaxX: int,
    forestMaxY: int,
) -> int:
    westView = westViewLen(forest, xIndex, yIndex, treeHeight)
    if westView != xIndex:
        westView += 1
    eastView = eastViewLen(forest, xIndex, yIndex, treeHeight, forestMaxX)
    if eastView != forestMaxX - xIndex:
        eastView += 1
    northView = northViewLen(forest, xIndex, yIndex, treeHeight)
    if northView != yIndex:
        northView += 1
    southView = southViewLen(forest, xIndex, yIndex, treeHeight, forestMaxY)
    if southView != forestMaxY - yIndex:
        southView += 1
    treeScore = westView * eastView * northView * southView
    return treeScore


def main() -> None:
    dataPath = Path(__file__).with_name("Data.txt")
    with open(dataPath) as dataFile:
        forestLines = enumerate(dataFile)
        forest: list[list[int]] = []
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
        for yIndex, treeLine in enumerate(forest):
            for xIndex, tree in enumerate(treeLine):
                if treeOnForestEdge(xIndex, yIndex, forestMaxX, forestMaxY):
                    treesVisibleFromOutside += 1
                elif treeTallEnoughToSee(
                    forest, tree, xIndex, yIndex, forestMaxX, forestMaxY
                ):
                    treesVisibleFromOutside += 1
                treeScore = getTreeScore(
                    forest, xIndex, yIndex, tree, forestMaxX, forestMaxY
                )
                if treeScore > bestTreeScore:
                    bestTreeScore = treeScore
        print(f"You can see {treesVisibleFromOutside} trees from outside")
        print(f"The best tree score is: {bestTreeScore}")


main()
