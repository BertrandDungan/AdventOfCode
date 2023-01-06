from pathlib import Path
from re import findall
from typing import Generator, Literal, Tuple, Union

CaveType = Union[Literal["#"], Literal["."], Literal["+"], Literal["o"]]


def addRocks(
    cave: list[list[CaveType]],
    caveShapes: list[list[Tuple[int, int]]],
    caveLowerBound: int,
) -> None:
    caveXOffset = caveLowerBound
    for line in caveShapes:
        for shapeCoord in line:
            cave[shapeCoord[1]][shapeCoord[0] - caveXOffset] = "#"


def getCaveBounds(caveShapes: list[list[Tuple[int, int]]]) -> Tuple[int, int, int]:
    lowestX = 500
    highestX = 500
    highestY = 0
    for line in caveShapes:
        for shape in line:
            xNumber = shape[0]
            yNumber = shape[1]
            if xNumber < lowestX:
                lowestX = xNumber
            elif xNumber > highestX:
                highestX = xNumber
            if yNumber > highestY:
                highestY = yNumber
    return lowestX, highestX + 1, highestY + 1


def findShapesInText(line: str) -> list[Tuple[int, int]]:
    shapeCords = findall(
        r"([0-9]+),([0-9]+)",
        line,
    )
    return [(int(coordPair[0]), int(coordPair[1])) for coordPair in shapeCords]


def getShapePoints(caveLines: list[str]) -> list[list[Tuple[int, int]]]:
    return [findShapesInText(line) for line in caveLines]


def pointToShapes(
    cavePoints: list[list[Tuple[int, int]]]
) -> list[list[Tuple[int, int]]]:
    return [list(fillBetweenPoints(point)) for point in cavePoints]


def fillBetweenPoints(
    pointLine: list[Tuple[int, int]]
) -> Generator[tuple[int, int], None, None]:
    lineRange = range(len(pointLine) - 1)
    for index in lineRange:
        yield pointLine[index]
        deltaX = range(
            pointLine[index][0],
            pointLine[index + 1][0],
            -1 if pointLine[index][0] > pointLine[index + 1][0] else 1,
        )
        deltaY = range(
            pointLine[index][1],
            pointLine[index + 1][1],
            -1 if pointLine[index][1] > pointLine[index + 1][1] else 1,
        )
        for increment in deltaX:
            yield (increment, pointLine[index][1])
        for increment in deltaY:
            yield (pointLine[index][0], increment)
    yield pointLine[-1]


def getCaveShapes(
    cavePoints: list[list[Tuple[int, int]]]
) -> list[list[Tuple[int, int]]]:
    return cavePoints


def addSandSource(cave: list[list[CaveType]], lowestX: int) -> None:
    cave[0][500 - lowestX] = "+"


def removeOldSandBlock(
    cave: list[list[CaveType]], sandPosition: Tuple[int, int]
) -> None:
    cave[sandPosition[1]][sandPosition[0]] = "."


def simulateFallingSand(
    lowestX: int, caveWidth: int, cave: list[list[CaveType]]
) -> None:
    caveHeight = len(cave)
    sandHasNotFallenOff = True
    while sandHasNotFallenOff:
        sandCanMove = True
        sandPosition: Tuple[int, int] = (500 - lowestX, 0)
        while sandCanMove:
            down = sandPosition[1] + 1
            right = sandPosition[0] + 1
            left = sandPosition[0] - 1
            if down > caveHeight - 1:
                sandHasNotFallenOff = False
                sandCanMove = False
                removeOldSandBlock(cave, sandPosition)
                break
            elif left < 0:
                sandHasNotFallenOff = False
                sandCanMove = False
                removeOldSandBlock(cave, sandPosition)
                break
            elif right > caveWidth - 1:
                sandHasNotFallenOff = False
                sandCanMove = False
                removeOldSandBlock(cave, sandPosition)
                break
            canMoveDown = cave[down][sandPosition[0]] == "."
            canMoveLeft = cave[down][left] == "."
            canMoveRight = cave[down][right] == "."
            if canMoveDown:
                removeOldSandBlock(cave, sandPosition)
                cave[down][sandPosition[0]] = "o"
                sandPosition = (sandPosition[0], down)
            elif canMoveLeft:
                removeOldSandBlock(cave, sandPosition)
                cave[down][left] = "o"
                sandPosition = (left, down)
            elif canMoveRight:
                removeOldSandBlock(cave, sandPosition)
                cave[down][right] = "o"
                sandPosition = (right, down)
            elif not canMoveDown and not canMoveLeft and not canMoveRight:
                sandCanMove = False
        if sandPosition[0] == 500 - lowestX and sandPosition[1] == 0:
            cave[0][500 - lowestX] = "o"
            sandHasNotFallenOff = False


def addFloor(cave: list[list[CaveType]], floorIndex: int, caveWidth: int) -> None:
    floor: list[CaveType] = ["#" for _ in range(caveWidth)]
    cave[floorIndex] = floor


def main() -> None:
    dataPath = Path(__file__).with_name("Data.txt")
    with open(dataPath) as dataFile:
        caveLines = dataFile.readlines()
        cavePoints = getShapePoints(caveLines)
        lowestX, highestX, highestY = getCaveBounds(cavePoints)
        caveWidth = highestX - lowestX
        caveShapes = pointToShapes(cavePoints)
        cave: list[list[CaveType]] = [
            ["." for _ in range(caveWidth)] for _ in range(highestY)
        ]
        addRocks(cave, caveShapes, lowestX)
        addSandSource(cave, lowestX)
        simulateFallingSand(lowestX, caveWidth, cave)

        numberOfSandBlocks = 0
        for caveRow in cave:
            numberOfSandBlocks += caveRow.count("o")
        print(f"There are {numberOfSandBlocks} blocks of sand in this cave")

        highestX = highestX * 2
        lowestX = lowestX // 2
        caveWidth = highestX - lowestX
        caveWithFloor: list[list[CaveType]] = [
            ["." for _ in range(caveWidth)] for _ in range(highestY + 2)
        ]
        addRocks(caveWithFloor, caveShapes, lowestX)
        addFloor(caveWithFloor, highestY + 1, caveWidth)
        simulateFallingSand(lowestX, caveWidth, caveWithFloor)
        numberOfSandBlocks = 0
        for caveRow in caveWithFloor:
            numberOfSandBlocks += caveRow.count("o")
        print(f"There are {numberOfSandBlocks} blocks of sand in this cave")


main()
