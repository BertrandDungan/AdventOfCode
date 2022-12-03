from enum import Enum
from pathlib import Path
from re import findall
from typing import Literal, TypeAlias

FirstStrategyPart: TypeAlias = Literal["A"] | Literal["B"] | Literal["C"]
SecondStrategyPart: TypeAlias = Literal["X"] | Literal["Y"] | Literal["Z"]
Move: TypeAlias = Literal["Rock"] | Literal["Paper"] | Literal["Scissors"]
Results: TypeAlias = Literal["Lose"] | Literal["Draw"] | Literal["Win"]


class OpponentMove(Enum):
    A = "Rock"
    B = "Paper"
    C = "Scissors"


class PlayerMove(Enum):
    X = "Rock"
    Y = "Paper"
    Z = "Scissors"


class MoveToBeat(Enum):
    Rock = "Scissors"
    Paper = "Rock"
    Scissors = "Paper"


class MoveToLose(Enum):
    Scissors = "Rock"
    Rock = "Paper"
    Paper = "Scissors"


class MoveScore(Enum):
    Rock = 1
    Paper = 2
    Scissors = 3


class ResultScore(Enum):
    Lose = 0
    Draw = 3
    Win = 6


class DesiredResult(Enum):
    X = "Lose"
    Y = "Draw"
    Z = "Win"


def getResultScore(player: OpponentMove, opponent: PlayerMove) -> int:
    if player.value == opponent.value:
        return ResultScore.Draw.value
    if MoveToBeat[opponent.value].value == player.value:
        return ResultScore.Win.value
    return ResultScore.Lose.value


def getStrategyFromLine(line: str) -> tuple[FirstStrategyPart, SecondStrategyPart]:
    matchingStrategy = findall(r"([A-C]) ([X-Z])", line)
    return (matchingStrategy[0][0], matchingStrategy[0][1])


def getIncompleteStrategyValue(
    strategy: tuple[FirstStrategyPart, SecondStrategyPart]
) -> int:
    opponentMove = OpponentMove[strategy[0]]
    playerMove = PlayerMove[strategy[1]]
    return getResultScore(opponentMove, playerMove) + MoveScore[playerMove.value].value


def getMatchingMove(move: Move, desiredResult: Results) -> Move:
    if desiredResult == "Draw":
        return move
    if desiredResult == "Win":
        return MoveToLose[move].value
    return MoveToBeat[move].value


def getElfStrategyValue(strategy: tuple[FirstStrategyPart, SecondStrategyPart]) -> int:
    desiredResult = DesiredResult[strategy[1]].value
    move = getMatchingMove(OpponentMove[strategy[0]].value, desiredResult)
    return ResultScore[desiredResult].value + MoveScore[move].value


dataPath = Path(__file__).with_name("Data.txt")
with open(dataPath) as dataFile:
    strategyLines = [getStrategyFromLine(line) for line in dataFile]
    incompleteScore = 0
    elfScore = 0
    for strategy in strategyLines:
        incompleteScore += getIncompleteStrategyValue(strategy)
        elfScore += getElfStrategyValue(strategy)
    print(f"Incomplete score: {incompleteScore}")
    print(f"Elf score: {elfScore}")
