from dataclasses import dataclass
from pathlib import Path
from re import search


@dataclass(frozen=True)
class RopePiece:
    x_position: int
    y_position: int


def moveHead(command: str, ropeHead: RopePiece) -> RopePiece:
    match command:
        case "U":
            return RopePiece(ropeHead.x_position, ropeHead.y_position + 1)
        case "D":
            return RopePiece(ropeHead.x_position, ropeHead.y_position - 1)
        case "L":
            return RopePiece(ropeHead.x_position - 1, ropeHead.y_position)
        case "R":
            return RopePiece(ropeHead.x_position + 1, ropeHead.y_position)
    raise Exception("No matching command found")


def addVisitIfNew(ropeTail: RopePiece, placesVisitedByTail: set[str]) -> set[str]:
    placesVisitedByTail.add(f"{ropeTail.x_position},{ropeTail.y_position}")
    return placesVisitedByTail


def moveTail(ropeHead: RopePiece, ropeTail: RopePiece) -> RopePiece:
    if (
        ropeHead.y_position == ropeTail.y_position
        and ropeHead.x_position == ropeTail.x_position
    ):
        return ropeTail
    if ropeHead.y_position == ropeTail.y_position:
        if ropeHead.x_position > ropeTail.x_position + 1:
            return RopePiece(ropeTail.x_position + 1, ropeTail.y_position)
        if ropeHead.x_position < ropeTail.x_position - 1:
            return RopePiece(ropeTail.x_position - 1, ropeTail.y_position)
    if ropeHead.x_position == ropeTail.x_position:
        if ropeHead.y_position > ropeTail.y_position + 1:
            return RopePiece(ropeTail.x_position, ropeTail.y_position + 1)
        if ropeHead.y_position < ropeTail.y_position - 1:
            return RopePiece(ropeTail.x_position, ropeTail.y_position - 1)
    if (
        ropeHead.x_position > ropeTail.x_position + 1
        or ropeHead.x_position < ropeTail.x_position - 1
        or ropeHead.y_position > ropeTail.y_position + 1
        or ropeHead.y_position < ropeTail.y_position - 1
    ):
        if ropeHead.x_position > ropeTail.x_position:
            if ropeHead.y_position > ropeTail.y_position:
                return RopePiece(ropeTail.x_position + 1, ropeTail.y_position + 1)
            if ropeHead.y_position < ropeTail.y_position:
                return RopePiece(ropeTail.x_position + 1, ropeTail.y_position - 1)
        if ropeHead.x_position < ropeTail.x_position:
            if ropeHead.y_position > ropeTail.y_position:
                return RopePiece(ropeTail.x_position - 1, ropeTail.y_position + 1)
            if ropeHead.y_position < ropeTail.y_position:
                return RopePiece(ropeTail.x_position - 1, ropeTail.y_position - 1)
    return ropeTail


def interpretMove(command: str) -> tuple[str, int]:
    searchResult = search(r"^([A-Z]) ([0-9]+)", command)
    assert searchResult is not None
    return (searchResult[1], int(searchResult[2]))


def performCommand(
    command: str,
    ropeHead: RopePiece,
    ropeList: list[RopePiece],
    placesVisitedByTail: set[str],
) -> tuple[RopePiece, list[RopePiece], set[str]]:
    directionToMove, magnitude = interpretMove(command)
    for _ in range(magnitude):
        ropeHead = moveHead(directionToMove, ropeHead)
        for index, rope in enumerate(ropeList):
            if index == 0:
                ropeList[index] = moveTail(ropeHead, rope)
            else:
                ropeList[index] = moveTail(ropeList[index - 1], rope)
        placesVisitedByTail = addVisitIfNew(ropeList[-1], placesVisitedByTail)
    return (ropeHead, ropeList, placesVisitedByTail)


def main() -> None:
    dataPath = Path(__file__).with_name("Data.txt")
    with open(dataPath) as dataFile:
        ropeHead = RopePiece(0, 0)
        ropeTail = [RopePiece(0, 0)]
        placesVisitedByTail: set[str] = {"0,0"}
        for command in dataFile:
            ropeHead, ropeTail, placesVisitedByTail = performCommand(
                command, ropeHead, ropeTail, placesVisitedByTail
            )

        print(f"Tail visits {len(placesVisitedByTail)} spots with 2 piece rope")

        dataFile.seek(0)
        tenPieceRopeHead = RopePiece(0, 0)
        tenPieceRopeTail = [
            RopePiece(0, 0),
            RopePiece(0, 0),
            RopePiece(0, 0),
            RopePiece(0, 0),
            RopePiece(0, 0),
            RopePiece(0, 0),
            RopePiece(0, 0),
            RopePiece(0, 0),
            RopePiece(0, 0),
        ]
        placesVisitedByTenPieceTail: set[str] = {"0,0"}
        for command in dataFile:
            (
                tenPieceRopeHead,
                tenPieceRopeTail,
                placesVisitedByTenPieceTail,
            ) = performCommand(
                command, tenPieceRopeHead, tenPieceRopeTail, placesVisitedByTenPieceTail
            )
        print(
            f"Tail visits {len(placesVisitedByTenPieceTail)} spots with 10 piece rope"
        )


main()
