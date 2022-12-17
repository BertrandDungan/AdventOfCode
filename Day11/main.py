from dataclasses import dataclass
from functools import reduce
from operator import add, mul
from pathlib import Path
from re import findall
from typing import Callable


@dataclass()
class Monkey:
    items: list[int]
    operation: Callable[[int], int]
    testDivision: int
    truthMonkey: int
    falseMonkey: int
    inspections: int


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


def main() -> None:
    dataPath = Path(__file__).with_name("Data.txt")
    with open(dataPath) as dataFile:
        file = dataFile.read()
        monkeyMatches = findall(
            r": ((?:[0-9]+|, [0-9]+)+)\n.+= old (.+) ((?:[0-9]+)|(?:old))\n.+ ([0-9]+)\n.+([0-9]+)\n.+([0-9])",
            file,
        )
        monkeyList: list[Monkey] = []
        for monkey in monkeyMatches:
            monkeyItems: str = monkey[0]
            operator: str = monkey[1]
            operand: str = monkey[2]
            monkeyList.append(
                Monkey(
                    [int(item) for item in monkeyItems.split(",")],
                    partialMonkeyOperation(operand, operatorToFunc(operator)),
                    int(monkey[3]),
                    int(monkey[4]),
                    int(monkey[5]),
                    0,
                )
            )
        # for _ in range(20):
        #     for monkey in monkeyList:
        #         for item in monkey.items:
        #             monkey.inspections += 1
        #             worry = monkey.operation(item) // 3
        #             if worry % monkey.testDivision < 1:
        #                 monkeyList[monkey.truthMonkey].items.append(worry)
        #             else:
        #                 monkeyList[monkey.falseMonkey].items.append(worry)
        #         monkey.items = []
        # monkeyList.sort(key=lambda monkey: monkey.inspections)
        # smallMonkeyBusiness = monkeyList[-1].inspections * monkeyList[-2].inspections
        # print(monkeyList[-1].inspections)
        # print(monkeyList[-2].inspections)
        # print(f"Monkey business with less worry = {smallMonkeyBusiness}")

        product_of_all_divisors: int = reduce(
            mul, [monkey.testDivision for monkey in monkeyList]
        )

        for _ in range(10_000):
            for monkey in monkeyList:
                for item in monkey.items:
                    monkey.inspections += 1
                    worry = monkey.operation(item) % product_of_all_divisors
                    if worry % monkey.testDivision < 1:
                        monkeyList[monkey.truthMonkey].items.append(worry)
                    else:
                        monkeyList[monkey.falseMonkey].items.append(worry)
                monkey.items = []
        monkeyList.sort(key=lambda monkey: monkey.inspections)
        maxMonkeyBusiness = monkeyList[-1].inspections * monkeyList[-2].inspections
        print(f"Max Monkey business = {maxMonkeyBusiness}")
        print(monkeyList[-1].inspections)
        print(monkeyList[-2].inspections)
        print(f"Max Monkey business = {2_713_310_158}")


main()
