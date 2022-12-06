from functools import reduce
from io import TextIOWrapper
from pathlib import Path
from typing import Iterable


def getTotalCalories(file: TextIOWrapper) -> Iterable[int]:
    caloriesList = []
    numRegister = 0
    for line in file:
        if line == "\n":
            caloriesList.append(numRegister)
            numRegister = 0
        else:
            numRegister += int(line)
    return caloriesList


dataPath = Path(__file__).with_name("Data.txt")
with open(dataPath) as dataFile:
    elfCalorieList = getTotalCalories(dataFile)
    print(f"Highest elf calories = {reduce(max, elfCalorieList)}")
    sortedElfCalories = sorted(elfCalorieList, reverse=True)
    topThreeElfCalories = sum(sortedElfCalories[0:3])
    print(f"Top three elf calories combined = {topThreeElfCalories}")
