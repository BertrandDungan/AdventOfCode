from pathlib import Path
from re import compile, findall, search


class Move:
    def __init__(self, quantity: str, moveFrom: str, moveTo: str) -> None:
        self.moveFrom = int(moveFrom)
        self.moveTo = int(moveTo)
        self.quantity = int(quantity)


def getBiggestStackNumber(file: list[str]) -> int:
    stackNumbersRegEx = compile(r"([0-9]+) \n")
    for line in file:
        biggestStack = search(stackNumbersRegEx, line)
        if biggestStack:
            return int(biggestStack[0])
    return 0


def getStartingStacks(file: list[str]) -> list[list[str]]:
    stackRegEx = compile(r"\[(.)\]|(    )")
    biggestStack = getBiggestStackNumber(file)
    stackAccumulator = [list() for _ in range(biggestStack)]
    for line in file:
        cargoOnLine = findall(stackRegEx, line)
        for index, cargoMatch in enumerate(cargoOnLine):
            cargo = cargoMatch[0]
            if cargo != "":
                stackAccumulator[index].insert(0, cargo)

    return stackAccumulator


def getMoves(file: list[str]) -> list[Move]:
    moveRegEx = compile(r"([0-9]+).{6}([0-9]+).{4}([0-9]+)")
    moveAccumulator = []
    for line in file:
        foundMoves = findall(moveRegEx, line)
        if len(foundMoves) > 0:
            moveAccumulator.append(
                Move(foundMoves[0][0], foundMoves[0][1], foundMoves[0][2])
            )
    return moveAccumulator


def crane9000Move(move: Move, cargo: list[list[str]]) -> None:
    for _ in range(move.quantity):
        cargo[move.moveTo - 1].append(cargo[move.moveFrom - 1].pop())


def crane9001Move(move: Move, cargo: list[list[str]]) -> None:
    cargo[move.moveTo - 1].extend(cargo[move.moveFrom - 1][-move.quantity:])
    cargo[move.moveFrom - 1] = cargo[move.moveFrom - 1][:-move.quantity]


def getTopCargo(cargo: list[list[str]]) -> list[str]:
    return [crateStack.pop() for crateStack in cargo]


dataPath = Path(__file__).with_name("Data.txt")
with open(dataPath) as dataFile:
    entireFile = dataFile.readlines()
    cargo9000Stack = getStartingStacks(entireFile)
    cargo9001Stack = getStartingStacks(entireFile)
    moves = getMoves(entireFile)
    for move in moves:
        crane9000Move(move, cargo9000Stack)
        crane9001Move(move, cargo9001Stack)
    topCargo9000 = getTopCargo(cargo9000Stack)
    topCargo9001 = getTopCargo(cargo9001Stack)
    print(f"The top cargo stacked by the 9000 are: {topCargo9000}")
    print(f"The top cargo stacked by the 9001 are: {topCargo9001}")
