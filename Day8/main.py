from pathlib import Path


def treeOnForestEdge(
    xIndex: int, yIndex: int, forestMaxX: int, forestMaxY: int
) -> bool:
    return xIndex == 0 or yIndex == 0 or xIndex == forestMaxX or yIndex == forestMaxY


def treeTallEnoughToSee(
    forest: list[list[int]],
    treeHeight: int,
    xIndex: int,
    yIndex: int,
    forestMaxX: int,
    forestMaxY: int,
) -> bool:
    westView = [tree for tree in forest[yIndex][0:xIndex] if tree < treeHeight]
    if len(westView) == xIndex:
        return True
    eastView = [
        tree
        for tree in forest[yIndex][xIndex + 1 : forestMaxX + 1]
        if tree < treeHeight
    ]
    if len(eastView) == forestMaxX - xIndex:
        return True
    northView = [tree[xIndex] for tree in forest[0:yIndex] if tree[xIndex] < treeHeight]
    if len(northView) == yIndex:
        return True
    southView = [
        tree[xIndex]
        for tree in forest[yIndex + 1 : forestMaxY + 1]
        if tree[xIndex] < treeHeight
    ]
    if len(southView) == forestMaxY - yIndex:
        return True
    return False


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
            # treeScore = getTreeScore(blockingTrees, tree, forestMaxY, forestMaxX)
            # if treeScore > bestTreeScore:
            #     bestTreeScore = treeScore
            # bestTree = tree
    print(f"You can see {treesVisibleFromOutside} trees from outside")
    print(f"The best tree score is: {bestTreeScore}")
