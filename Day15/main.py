from itertools import chain
from pathlib import Path
from re import findall
from typing import TypeVar

T = TypeVar("T")
ROW_POSITION = 10


def getSensorPairs(sensorData: str) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    matches = findall(
        r"x=([-?0-9]+), y=([-?0-9]+).+x=([-?0-9]+), y=([-?0-9]+)", sensorData
    )
    return [
        (
            (
                int(sensorBeaconPair[0]),
                int(sensorBeaconPair[1]),
            ),
            (
                int(sensorBeaconPair[2]),
                int(sensorBeaconPair[3]),
            ),
        )
        for sensorBeaconPair in matches
    ]


def calcDistance(x1: int, x2: int, y1: int, y2: int) -> int:
    return abs(x1 - x2) + abs(y1 - y2)


def addTaxiDistance(
    sensorPairs: list[tuple[tuple[int, int], tuple[int, int]]]
) -> list[tuple[tuple[int, int], tuple[int, int], int]]:
    return [
        (
            sensorBeacon[0],
            sensorBeacon[1],
            calcDistance(
                sensorBeacon[0][0],
                sensorBeacon[1][0],
                sensorBeacon[0][1],
                sensorBeacon[1][1],
            ),
        )
        for sensorBeacon in sensorPairs
    ]


def getBoundingSensorArea(
    sensorsWithDistance: list[tuple[tuple[int, int], tuple[int, int], int]]
) -> list[
    tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int], int]
]:
    return [
        (
            (sensorPair[0][0], sensorPair[0][1] + sensorPair[2]),
            (sensorPair[0][0] + sensorPair[2], sensorPair[0][1]),
            (sensorPair[0][0] - sensorPair[2], sensorPair[0][1]),
            (sensorPair[0][0], sensorPair[0][1] - sensorPair[2]),
            sensorPair[2],
        )
        for sensorPair in sensorsWithDistance
    ]


def getNorthWestLine(
    sensorCoords: tuple[
        tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int], int
    ],
    index: int,
) -> tuple[int, int]:
    return (sensorCoords[0][0] + index, sensorCoords[0][1] - index)


def getEastNorthLine(
    sensorCoords: tuple[
        tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int], int
    ],
    index: int,
) -> tuple[int, int]:
    return (sensorCoords[1][0] - index, sensorCoords[1][1] - index)


def getWestSouthLine(
    sensorCoords: tuple[
        tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int], int
    ],
    index: int,
) -> tuple[int, int]:
    return (sensorCoords[2][0] + index, sensorCoords[2][1] + index)


def getSouthEastLine(
    sensorCoords: tuple[
        tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int], int
    ],
    index: int,
) -> tuple[int, int]:
    return (sensorCoords[3][0] - index, sensorCoords[3][1] + index)


def getLinesBetweenCorners(
    sensorCoords: tuple[
        tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int], int
    ]
) -> list[tuple[int, int]]:
    return [
        getLine(sensorCoords, x)
        for x in range(sensorCoords[4])
        for getLine in (
            getNorthWestLine,
            getEastNorthLine,
            getWestSouthLine,
            getSouthEastLine,
        )
    ]


def getJustSensorArea(
    sensorArea: tuple[
        tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int], int
    ]
) -> list[tuple[int, int]]:
    return list(sensorArea[0:4])


def getSensorLines(
    boundingSensorArea: list[
        tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int], int]
    ]
) -> list[list[tuple[int, int]]]:
    return [
        getLinesBetweenCorners(sensorCoords) + getJustSensorArea(sensorCoords)
        for sensorCoords in boundingSensorArea
    ]


def getSensorLimits(sensorLines: list[tuple[int, int]]) -> tuple[int, int]:
    sortedSensorLines = sorted(sensorLines, key=lambda sensor: sensor[0])
    return sortedSensorLines[0][0], sortedSensorLines[-1][0]


def pointsInLine(lineLength: int, minX: int, coordinate: int) -> list[tuple[int, int]]:
    return [(line, lineLength) for line in range(minX, coordinate + 1)]


def getNumberOfIntersects(
    pointsInLine: list[tuple[int, int]],
    sensorAreaLines: list[tuple[int, int]],
) -> int:
    intersects = len(
        [point for point in sensorAreaLines if point in pointsInLine and point]
    )
    if intersects == 2 and pointsInLine[-1] in sensorAreaLines:
        return 3
    return intersects


def isOdd(number: int) -> bool:
    return number % 2 != 0


def getIntersectsForAllPointsInLine(
    minX: int,
    maxX: int,
    sensorAreaLines: list[list[tuple[int, int]]],
    beaconLocations: list[tuple[int, int]],
):
    non_empty_point_groups = [
        pointGroup
        for pointGroup in [
            [
                sensorPoint
                for sensorPoint in sensorAreaGroup
                if sensorPoint[1] == ROW_POSITION
            ]
            for sensorAreaGroup in sensorAreaLines
        ]
        if len(pointGroup) > 0
    ]
    for coordinate in range(minX, maxX):
        if not (coordinate, ROW_POSITION) in beaconLocations:
            linePoints = pointsInLine(ROW_POSITION, minX, coordinate)
            for sensorArea in non_empty_point_groups:
                intersects = getNumberOfIntersects(linePoints, sensorArea)
                if isOdd(intersects):
                    yield coordinate
                    break


def flatten(inputList: list[list[T]]) -> list[T]:
    return list(chain.from_iterable(inputList))


def main() -> None:
    dataPath = Path(__file__).with_name("Test.txt")
    with open(dataPath) as dataFile:
        sensorPairs = getSensorPairs(dataFile.read())
        pairsWithTaxiDistance = addTaxiDistance(sensorPairs)
        boundingSensorArea = getBoundingSensorArea(pairsWithTaxiDistance)
        sensorAreaLines = getSensorLines(boundingSensorArea)
        minX, maxX = getSensorLimits(flatten(sensorAreaLines))
        beaconLocations = [beacon[1] for beacon in sensorPairs]
        intersects = getIntersectsForAllPointsInLine(
            minX, maxX, sensorAreaLines, beaconLocations
        )
        numberOfIntersects = len(list(intersects))
        print(numberOfIntersects)


main()
