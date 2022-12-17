from dataclasses import dataclass
from functools import reduce
from operator import add, mul
from pathlib import Path
from re import findall
from typing import Any, Callable, Optional


@dataclass()
class Monkey:
    items: list[int]
    operation: Callable[[int], int]
    testDivision: int
    truthMonkey: int
    falseMonkey: int
    inspections: int = 0


def operatorToFunc(operator: str) -> Callable[[int, int], int]:
    if operator == "*":
        return mul
    if operator == "+":
        return add
    raise Exception(f"No valid operator found for {operator}")


def partialMonkeyOperation(
    operand: str, baseFunction: Callable[[int, int], int]
) -> Callable[[int], int]:
    if operand == "old":
        return lambda number: pow(number, 2)
    return lambda number: baseFunction(number, int(operand))


def calcMonkeyBusiness(
    rounds: int, monkeyList: list[Monkey], modulo: Optional[int] = None
) -> int:
    for _ in range(rounds):
        for monkey in monkeyList:
            for item in monkey.items:
                monkey.inspections += 1
                worry = (
                    monkey.operation(item) % modulo
                    if modulo
                    else monkey.operation(item) // 3
                )
                if worry % monkey.testDivision < 1:
                    monkeyList[monkey.truthMonkey].items.append(worry)
                else:
                    monkeyList[monkey.falseMonkey].items.append(worry)
            monkey.items = []
    monkeyList.sort(key=lambda monkey: monkey.inspections)
    return monkeyList[-1].inspections * monkeyList[-2].inspections


def createMonkeys(monkeyMatches: list[Any]) -> list[Monkey]:
    return [
        Monkey(
            [int(item) for item in monkey[0].split(",")],
            partialMonkeyOperation(monkey[2], operatorToFunc(monkey[1])),
            int(monkey[3]),
            int(monkey[4]),
            int(monkey[5]),
        )
        for monkey in monkeyMatches
    ]


def main() -> None:
    dataPath = Path(__file__).with_name("Data.txt")
    with open(dataPath) as dataFile:
        file = dataFile.read()
        monkeyMatches = findall(
            r": ((?:[0-9]+|, [0-9]+)+)\n.+= old (.+) ((?:[0-9]+)|(?:old))\n.+ ([0-9]+)\n.+([0-9]+)\n.+([0-9])",
            file,
        )
        smallMonkeyBusiness = calcMonkeyBusiness(20, createMonkeys(monkeyMatches))
        print(f"20 Monkey business with less worry = {smallMonkeyBusiness}")

        product_of_all_divisors: int = reduce(
            mul, [int(monkey[3]) for monkey in monkeyMatches]
        )
        maxMonkeyBusiness = calcMonkeyBusiness(
            10_000, createMonkeys(monkeyMatches), product_of_all_divisors
        )
        print(f"10,000 Max Monkey business = {maxMonkeyBusiness}")


main()
