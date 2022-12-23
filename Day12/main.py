import math
from dataclasses import dataclass
from io import TextIOWrapper
from pathlib import Path
from typing import Optional, TypeVar

T = TypeVar("T")


@dataclass()
class Node:
    height: str
    position: tuple[int, int]
    distanceToStart: Optional[int] = None


def generateMap(file: TextIOWrapper, allAZero=False) -> list[list[Node]]:
    return [
        [
            Node(
                character,
                (columnNumber, rowNumber),
                0 if allAZero and character == "a" else None,
            )
            for columnNumber, character in enumerate(lineText)
            if character != "\n"
        ]
        for rowNumber, lineText in enumerate(file)
    ]


def canTraverse(currentHeight: str, comparisonHeight: str) -> bool:
    return (
        currentHeight >= comparisonHeight
        or ord(currentHeight) == ord(comparisonHeight) - 1
    )


def nodeNeighbourGenerator(currentNode: Node, mapHeight: int, mapWidth: int):
    xPosition, yPosition = currentNode.position
    if xPosition < mapWidth - 1:
        yield (xPosition + 1, yPosition)
    if xPosition > 0:
        yield (xPosition - 1, yPosition)
    if yPosition < mapHeight - 1:
        yield (xPosition, yPosition + 1)
    if yPosition > 0:
        yield (xPosition, yPosition - 1)


def flatten(listOfLists: list[list[T]]) -> list[T]:
    return [item for listOfItems in listOfLists for item in listOfItems]


def dijkstraSearch(
    map: list[list[Node]], start: tuple[int, int], end: tuple[int, int]
) -> int:
    mapHeight = len(map)
    mapWidth = len(map[0])
    currentNode = map[start[1]][start[0]]
    unvisitedNodes = flatten(map)

    # Set distance to 0 as it is the start
    currentNode.distanceToStart = 0
    currentNode.height = "a"

    # Set end to have height z
    map[end[1]][end[0]].height = "z"

    while len(unvisitedNodes) > 0:
        unvisitedNodes = sorted(
            unvisitedNodes,
            key=lambda node: node.distanceToStart
            if node.distanceToStart is not None
            else math.inf,
        )
        currentNode = unvisitedNodes[0]
        for node in nodeNeighbourGenerator(currentNode, mapHeight, mapWidth):
            comparisonNode = map[node[1]][node[0]]
            assert currentNode.distanceToStart is not None
            if canTraverse(currentNode.height, comparisonNode.height):
                if node[0] == end[0] and node[1] == end[1]:
                    return currentNode.distanceToStart + 1
                if (
                    comparisonNode.distanceToStart is None
                    or comparisonNode.distanceToStart > currentNode.distanceToStart
                ):
                    comparisonNode.distanceToStart = currentNode.distanceToStart + 1
        unvisitedNodes = [
            stillUnvisited
            for stillUnvisited in unvisitedNodes
            if stillUnvisited.position[0] != currentNode.position[0]
            or stillUnvisited.position[1] != currentNode.position[1]
        ]
    raise Exception("No path found")


def main() -> None:
    dataPath = Path(__file__).with_name("Data.txt")
    with open(dataPath) as dataFile:
        STARTING_POSITION = (0, 20)
        END_POSITION = (135, 20)
        map: list[list[Node]] = generateMap(dataFile)
        dataFile.seek(0)
        distanceFromStart = dijkstraSearch(map, STARTING_POSITION, END_POSITION)
        print(f"The shortest path from the start takes {distanceFromStart} steps")
        mapA: list[list[Node]] = generateMap(dataFile, True)
        distanceFromAnyA = dijkstraSearch(mapA, STARTING_POSITION, END_POSITION)
        print(f"The shortest path from any 'a' takes {distanceFromAnyA} steps")


main()
