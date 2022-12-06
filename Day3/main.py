from functools import reduce
from itertools import chain, islice
from operator import add
from pathlib import Path
from typing import Iterable, List, Tuple, TypeVar

T = TypeVar("T")


def splitRucksack(rucksack: str) -> Tuple[str, str]:
    firstHalf = rucksack[: len(rucksack) // 2]
    secondHalf = rucksack[len(rucksack) // 2:]
    return (firstHalf, secondHalf)


def checkIfInRucksack(item: str, rucksack: str) -> bool:
    return item in rucksack


def findCommonItems(rucksack: str):
    rucksackHalves = splitRucksack(rucksack)
    return list(
        *set(
            filter(
                lambda item: checkIfInRucksack(item, rucksackHalves[1]),
                rucksackHalves[0],
            )
        )
    )


def getItemPriority(item: str) -> int:
    asciiOffset = 96 if item.islower() else 38
    return ord(item) - asciiOffset


def flatten(inputList: List[List[T]]) -> List[T]:
    return list(chain.from_iterable(inputList))


def batched(iterable: Iterable[T], chuckSize: int) -> Iterable[List[T]]:
    it = iter(iterable)
    while True:
        batch = list(islice(it, chuckSize))
        if not batch:
            return
        yield batch


def findBadge(elfGroup: List[str]) -> str:
    firstRucksack = elfGroup[0]
    for item in firstRucksack:
        if checkIfInRucksack(item, elfGroup[1]) and checkIfInRucksack(
            item, elfGroup[2]
        ):
            return item
    return ''


dataPath = Path(__file__).with_name("Data.txt")
with open(dataPath) as dataFile:
    commonItems = [findCommonItems(rucksack) for rucksack in dataFile]
    flattenedItems = flatten(commonItems)
    itemPriorities = [getItemPriority(item) for item in flattenedItems]
    priorityTotal = reduce(add, itemPriorities)
    print(f'Rucksack total priority: {priorityTotal}')
    dataFile.seek(0)
    elfGroups = batched(dataFile, 3)
    elfBadges = map(findBadge, elfGroups)
    badgePriorities = [getItemPriority(item) for item in elfBadges]
    badgeTotal = reduce(add, badgePriorities)
    print(f'Badge total priority: {badgeTotal}')
