from enum import Enum
from pathlib import Path
from re import findall
from typing import Generator, Literal, NamedTuple, TypeVar

T = TypeVar("T")
# ROW_POSITION = 2_000_000
ROW_POSITION = 10
Point = NamedTuple("Point", [("x", int), ("y", int)])
Line = NamedTuple("Line", [("start", Point), ("end", Point)])


class Orientation(Enum):
    Clockwise = 1
    Anticlockwise = 2
    Collinear = 3


def getSensorPairs(sensorData: str) -> list[Line]:
    matches = findall(
        r"x=([-?0-9]+), y=([-?0-9]+).+x=([-?0-9]+), y=([-?0-9]+)", sensorData
    )
    return [
        Line(
            Point(
                int(sensorBeaconPair[0]),
                int(sensorBeaconPair[1]),
            ),
            Point(
                int(sensorBeaconPair[2]),
                int(sensorBeaconPair[3]),
            ),
        )
        for sensorBeaconPair in matches
    ]


def calcDistance(x1: int, x2: int, y1: int, y2: int) -> int:
    return abs(x1 - x2) + abs(y1 - y2)


def addTaxiDistance(sensorPairs: list[Line]) -> list[tuple[Point, Point, int]]:
    return [
        (
            sensorBeacon.start,
            sensorBeacon.end,
            calcDistance(
                sensorBeacon.start.x,
                sensorBeacon.end.x,
                sensorBeacon.start.y,
                sensorBeacon.end.y,
            ),
        )
        for sensorBeacon in sensorPairs
    ]


def getBoundingSensorArea(
    sensorsWithDistance: list[tuple[Point, Point, int]]
) -> list[tuple[Line, Line, Line, Line]]:
    return [
        (
            Line(
                Point(sensorPair[0].x, sensorPair[0].y + sensorPair[2]),  # S
                Point(sensorPair[0].x + sensorPair[2], sensorPair[0].y),  # E
            ),
            Line(
                Point(sensorPair[0].x + sensorPair[2], sensorPair[0].y),  # E
                Point(sensorPair[0].x, sensorPair[0].y - sensorPair[2]),  # N
            ),
            Line(
                Point(sensorPair[0].x, y=sensorPair[0].y - sensorPair[2]),  # N
                Point(sensorPair[0].x - sensorPair[2], sensorPair[0].y),  # W
            ),
            Line(
                Point(sensorPair[0].x - sensorPair[2], sensorPair[0].y),  # W
                Point(sensorPair[0].x, sensorPair[0].y + sensorPair[2]),  # S
            ),
        )
        for sensorPair in sensorsWithDistance
    ]


def getSensorLimits(
    sensorPoints: list[
        tuple[
            Line,
            Line,
            Line,
            Line,
        ]
    ]
) -> tuple[int, int]:
    lowestX = sensorPoints[0][0].start.x
    highestX = sensorPoints[0][0].start.x
    for sensorArea in sensorPoints:
        for sensorPair in sensorArea:
            for sensor in sensorPair:
                sensorX = sensor.x
                if sensorX < lowestX:
                    lowestX = sensorX
                if sensorX > highestX:
                    highestX = sensorX
    return lowestX, highestX


def pointsInLine(lineLength: int, minX: int, coordinate: int) -> list[Point]:
    return [Point(line, lineLength) for line in range(minX, coordinate + 1)]


def getNumberOfIntersects(
    pointsInLine: list[Point],
    sensorAreaLines: list[Point],
) -> int:
    intersects = len(
        [point for point in sensorAreaLines if point in pointsInLine and point]
    )
    return intersects


def isOdd(number: int) -> bool:
    return number % 2 != 0


def get_orientation(point_1: Point, point_2: Point, point_3: Point) -> Orientation:
    anchorArea = (point_2.x - point_1.x) * (point_3.y - point_1.y) - (
        point_3.x - point_1.x
    ) * (point_2.y - point_1.y)
    if anchorArea > 0:
        return Orientation.Clockwise
    if anchorArea < 0:
        return Orientation.Anticlockwise
    return Orientation.Collinear


def isPointOnLine(
    linePoint1: Point,
    comparisonPoint: Point,
    linePoint2: Point,
) -> bool:
    crossproduct = (comparisonPoint.y - linePoint1.y) * (
        linePoint2.x - linePoint1.x
    ) - (comparisonPoint.x - linePoint1.x) * (linePoint2.y - linePoint1.y)
    if abs(crossproduct) != 0:
        return False
    dotProduct = (comparisonPoint.x - linePoint1.x) * (linePoint2.x - linePoint1.x) + (
        comparisonPoint.y - linePoint1.y
    ) * (linePoint2.y - linePoint1.y)
    if dotProduct < 0:
        return False
    squaredlengthba = (linePoint2.x - linePoint1.x) * (linePoint2.x - linePoint1.x) + (
        linePoint2.y - linePoint1.y
    ) * (linePoint2.y - linePoint1.y)
    if dotProduct > squaredlengthba:
        return False
    return True


def doLinesIntersect(
    line_1: Line,
    line_2: Line,
) -> bool:
    orientation_1 = get_orientation(line_1.start, line_1.end, line_2.start)
    orientation_2 = get_orientation(line_1.start, line_1.end, line_2.end)
    orientation_3 = get_orientation(line_2.start, line_2.end, line_1.start)
    orientation_4 = get_orientation(line_2.start, line_2.end, line_1.end)

    if orientation_1 != orientation_2 and orientation_3 != orientation_4:
        return True

    if orientation_1 == Orientation.Collinear and isPointOnLine(
        line_1.start, line_2.start, line_1.end
    ):
        return True

    if orientation_2 == Orientation.Collinear and isPointOnLine(
        line_1.start, line_2.end, line_1.end
    ):
        return True

    if orientation_3 == Orientation.Collinear and isPointOnLine(
        line_2.start, line_1.start, line_2.end
    ):
        return True

    if orientation_4 == Orientation.Collinear and isPointOnLine(
        line_2.start, line_1.end, line_2.end
    ):
        return True
    return False


def getIntersectsForPointsInLine(
    minX: int,
    maxX: int,
    sensorArea: list[
        tuple[
            Line,
            Line,
            Line,
            Line,
        ]
    ],
    beaconLocations: list[Point],
) -> Generator[Literal[1], None, None]:
    for coordinate in range(minX, maxX):
        if not (coordinate, ROW_POSITION) in beaconLocations:
            intersects = 0
            for sensorGroup in sensorArea:
                for sensorPair in sensorGroup:
                    if isPointOnLine(
                        sensorPair.start,
                        Point(coordinate, ROW_POSITION),
                        sensorPair.end,
                    ):
                        intersects = 1
                        break
                    if doLinesIntersect(
                        sensorPair,
                        Line(
                            Point(minX, ROW_POSITION), Point(coordinate, ROW_POSITION)
                        ),
                    ):
                        intersects += 1
                if isOdd(intersects):
                    yield 1
                    break


def main() -> None:
    dataPath = Path(__file__).with_name("Test.txt")
    with open(dataPath) as dataFile:
        sensorPairs = getSensorPairs(dataFile.read())
        pairsWithTaxiDistance = addTaxiDistance(sensorPairs)
        boundingSensorArea = getBoundingSensorArea(pairsWithTaxiDistance)
        minX, maxX = getSensorLimits(boundingSensorArea)
        beaconLocations = [beacon[1] for beacon in sensorPairs]
        intersects = getIntersectsForPointsInLine(
            minX, maxX, boundingSensorArea, beaconLocations
        )
        numberOfIntersects = sum(intersects)
        print(numberOfIntersects)


main()
