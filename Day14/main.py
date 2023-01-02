from pathlib import Path
from re import findall
from typing import Generator, Literal, Tuple, Union

CaveType = Union[Literal["#"], Literal["."], Literal["+"]]


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


def main() -> None:
    dataPath = Path(__file__).with_name("Test.txt")
    with open(dataPath) as dataFile:
        caveLines = dataFile.readlines()
        cavePoints = getShapePoints(caveLines)
        lowestX, highestX, highestY = getCaveBounds(cavePoints)
        caveWidth = range(highestX - lowestX)
        caveShapes = pointToShapes(cavePoints)
        cave: list[list[CaveType]] = [["." for _ in caveWidth] for _ in range(highestY)]
        addRocks(cave, caveShapes, lowestX)
        pass
        # sandMoving = True
        # while sandMoving:
        #     cave, sandMoving = simulateCave(cave)


main()
