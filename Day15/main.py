from enum import Enum
from pathlib import Path
from re import findall
from typing import Generator, Literal, NamedTuple, TypeVar

T = TypeVar("T")
ROW_POSITION = 2_000_000
# ROW_POSITION = 10
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


def addTaxiDistance(sensorPairs: list[Line]) -> list[tuple[Point, int]]:
    return [
        (
            sensorBeacon.start,
            calcDistance(
                sensorBeacon.start.x,
                sensorBeacon.end.x,
                sensorBeacon.start.y,
                sensorBeacon.end.y,
            ),
        )
        for sensorBeacon in sensorPairs
    ]


def getWestLine(sensorTaxi: tuple[Point, int]) -> int:
    return sensorTaxi[0].x - sensorTaxi[1]


def getEastLine(sensorTaxi: tuple[Point, int]) -> int:
    return sensorTaxi[0].x + sensorTaxi[1]


def getSensorLimits(sensorPoints: list[tuple[Point, int]]) -> tuple[int, int]:
    sensor_x_boundaries = [
        f(sensor) for sensor in sensorPoints for f in (getWestLine, getEastLine)
    ]
    return min(sensor_x_boundaries), max(sensor_x_boundaries)


def getIntersectsForPointsInLine(
    minX: int,
    maxX: int,
    sensorsWithTaxi: list[tuple[Point, int]],
    beaconLocations: list[Point],
) -> Generator[Literal[1], None, None]:
    for coordinate in range(minX, maxX):
        currentLocation = Point(coordinate, ROW_POSITION)
        if currentLocation not in beaconLocations:
            for sensor in sensorsWithTaxi:
                if (
                    calcDistance(
                        sensor[0].x, currentLocation.x, sensor[0].y, currentLocation.y
                    )
                    <= sensor[1]
                ):
                    yield 1
                    break


def main() -> None:
    dataPath = Path(__file__).with_name("Data.txt")
    with open(dataPath) as dataFile:
        sensorBeaconPair = getSensorPairs(dataFile.read())
        pairsWithTaxiDistance = addTaxiDistance(sensorBeaconPair)
        minX, maxX = getSensorLimits(pairsWithTaxiDistance)
        beaconLocations = [beacon[1] for beacon in sensorBeaconPair]
        intersects = getIntersectsForPointsInLine(
            minX, maxX, pairsWithTaxiDistance, beaconLocations
        )
        numberOfIntersects = sum(intersects)
        print(numberOfIntersects)


main()
