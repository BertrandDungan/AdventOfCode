from dataclasses import dataclass
from pathlib import Path
from re import search


@dataclass(frozen=True)
class RopeHead:
    x_position: int
    y_position: int


@dataclass(frozen=True)
class RopeTail:
    x_position: int
    y_position: int


def moveHead(command: str, ropeHead: RopeHead) -> RopeHead:
    match command:
        case "U":
            return RopeHead(ropeHead.x_position, ropeHead.y_position + 1)
        case "D":
            return RopeHead(ropeHead.x_position, ropeHead.y_position - 1)
        case "L":
            return RopeHead(ropeHead.x_position - 1, ropeHead.y_position)
        case "R":
            return RopeHead(ropeHead.x_position + 1, ropeHead.y_position)
    raise Exception("No matching command found")


def addVisitIfNew(ropeTail: RopeTail, placesVisitedByTail: set[str]) -> set[str]:
    placesVisitedByTail.add(f"{ropeTail.x_position}{ropeTail.y_position}")
    return placesVisitedByTail


def moveTail(ropeHead: RopeHead, ropeTail: RopeTail) -> RopeTail:
    new_x_pos = ropeTail.x_position
    new_y_pos = ropeTail.y_position
    if ropeHead.y_position == ropeTail.y_position:
        if ropeHead.x_position > ropeTail.x_position + 1:
            new_x_pos += 1
        elif ropeHead.x_position < ropeTail.x_position - 1:
            new_x_pos -= 1
    elif ropeHead.x_position == ropeTail.x_position:
        if ropeHead.y_position > ropeTail.y_position + 1:
            new_y_pos += 1
        elif ropeHead.y_position < ropeTail.y_position - 1:
            new_y_pos -= 1
    elif (
        ropeHead.y_position != ropeTail.y_position
        and ropeHead.x_position != ropeTail.x_position
        and (
            ropeHead.x_position > ropeTail.x_position + 1
            or ropeHead.x_position < ropeTail.x_position - 1
            or ropeHead.y_position > ropeTail.y_position + 1
            or ropeHead.y_position < ropeTail.y_position - 1
        )
    ):
        if ropeHead.x_position > ropeTail.x_position:
            if ropeHead.y_position > ropeTail.y_position:
                new_x_pos += 1
                new_y_pos += 1
            elif ropeHead.y_position < ropeTail.y_position:
                new_x_pos += 1
                new_y_pos -= 1
        elif ropeHead.x_position < ropeTail.x_position:
            if ropeHead.y_position > ropeTail.y_position:
                new_x_pos -= 1
                new_y_pos += 1

            elif ropeHead.y_position < ropeTail.y_position:
                new_x_pos -= 1
                new_y_pos -= 1

    return RopeTail(new_x_pos, new_y_pos)


def interpretMove(command: str) -> tuple[str, int]:
    searchResult = search(r"^([A-Z]) ([0-9]+)", command)
    assert searchResult is not None
    return (searchResult[1], int(searchResult[2]))


def performCommand(
    command: str,
    ropeHead: RopeHead,
    ropeTail: RopeTail,
    placesVisitedByTail: set[str],
) -> tuple[RopeHead, RopeTail, set[str]]:
    directionToMove, magnitude = interpretMove(command)
    for _ in range(magnitude):
        ropeHead = moveHead(directionToMove, ropeHead)
        ropeTail = moveTail(ropeHead, ropeTail)
        placesVisitedByTail = addVisitIfNew(ropeTail, placesVisitedByTail)
    return (ropeHead, ropeTail, placesVisitedByTail)


def main() -> None:
    dataPath = Path(__file__).with_name("Test.txt")
    with open(dataPath) as dataFile:
        ropeHead = RopeHead(0, 0)
        ropeTail = RopeTail(0, 0)
        placesVisitedByTail: set[str] = {"00"}
        for command in dataFile:
            ropeHead, ropeTail, placesVisitedByTail = performCommand(
                command, ropeHead, ropeTail, placesVisitedByTail
            )

        print(placesVisitedByTail)
        print(len(placesVisitedByTail))


main()
