from pathlib import Path
from re import findall


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


def getSensorLines(
    boundingSensorArea: list[
        tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int], int]
    ]
):
    for sensorCoords in boundingSensorArea:
        for length in range(sensorCoords[4]):
            yield (sensorCoords[0][0] - length, sensorCoords[0][1] + length)
            yield (sensorCoords[1][0] - length, sensorCoords[1][1] - length)
            yield (sensorCoords[2][0] + length, sensorCoords[2][1] + length)
            yield (sensorCoords[1][0] + length, sensorCoords[1][1] - length)


def getSensorLimits(sensorLines: list[tuple[int, int]]) -> tuple[int, int]:
    sortedSensorLines = sorted(sensorLines, key=lambda sensor: sensor[0])
    return sortedSensorLines[0][0], sortedSensorLines[-1][0]


def main() -> None:
    dataPath = Path(__file__).with_name("Test.txt")
    with open(dataPath) as dataFile:
        sensorPairs = getSensorPairs(dataFile.read())
        pairsWithTaxiDistance = addTaxiDistance(sensorPairs)
        boundingSensorArea = getBoundingSensorArea(pairsWithTaxiDistance)
        sensorAreaLines = list(getSensorLines(boundingSensorArea))
        minX, maxX = getSensorLimits(sensorAreaLines)
        infiniteLine = range(minX, maxX)
        for tuple in sensorAreaLines:
            print(tuple)


main()
