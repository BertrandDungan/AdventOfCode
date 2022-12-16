from dataclasses import dataclass
from operator import add, mul
from pathlib import Path
from re import findall
from typing import Callable

common_divisor = 100


@dataclass()
class Monkey:
    items: list[float]
    operation: Callable[[float], float]
    testDivision: int
    truthMonkey: int
    falseMonkey: int
    inspections: int


def operatorToFunc(operator: str) -> Callable[[float, float], float]:
    if operator == "*":
        return mul
    if operator == "+":
        return add
    raise Exception(f"No valid operator found for {operator}")


def partialMonkeyOperation(
    operand: str, baseFunction: Callable[[float, float], float]
) -> Callable[[float], float]:
    if operand == "old":
        return lambda number: pow(number / common_divisor, 2)
    return lambda number: baseFunction(number, int(operand) / common_divisor)


def main() -> None:
    dataPath = Path(__file__).with_name("Test.txt")
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
                    [float(item) / common_divisor for item in monkeyItems.split(",")],
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
        # print(f"Monkey business with less worry = {smallMonkeyBusiness}")

        # for _ in range(10_000):
        #     for monkey in monkeyList:
        #         for item in monkey.items:
        #             monkey.inspections += 1
        #             worry = monkey.operation(item)
        #             if worry % monkey.testDivision < 1:
        #                 monkeyList[monkey.truthMonkey].items.append(worry)
        #             else:
        #                 monkeyList[monkey.falseMonkey].items.append(worry)
        #         monkey.items = []
        # monkeyList.sort(key=lambda monkey: monkey.inspections)
        # maxMonkeyBusiness = monkeyList[-1].inspections * monkeyList[-2].inspections
        # print(f"Max Monkey business = {maxMonkeyBusiness}")
        # print(monkeyList[-1].inspections)
        # print(monkeyList[-2].inspections)
        # print(f"Max Monkey business = {2_713_310_158}")


main()
