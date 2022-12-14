from pathlib import Path
from re import findall
from typing import List


def getAssignments(line: str) -> List[int]:
    assignments = findall(r"([0-9]+)-([0-9]+),([0-9]+)-([0-9]+)", line)[0]
    return [int(number) for number in assignments]


def isFullyOverlapping(assignments: List[int]) -> bool:
    assignmentOneStart = assignments[0]
    assignmentOneEnd = assignments[1]
    assignmentTwoStart = assignments[2]
    assignmentTwoEnd = assignments[3]

    if (
        assignmentOneStart >= assignmentTwoStart
        and assignmentOneEnd <= assignmentTwoEnd
    ) or (
        assignmentTwoStart >= assignmentOneStart
        and assignmentTwoEnd <= assignmentOneEnd
    ):
        return True
    return False


def isOverlapping(assignments: List[int]) -> bool:
    assignmentOneStart = assignments[0]
    assignmentOneEnd = assignments[1]
    assignmentTwoStart = assignments[2]
    assignmentTwoEnd = assignments[3]
    if (
        (
            assignmentOneStart >= assignmentTwoStart
            and assignmentOneStart <= assignmentTwoEnd
        )
        or (
            assignmentOneEnd <= assignmentTwoEnd
            and assignmentOneEnd >= assignmentTwoStart
        )
        or (
            assignmentTwoStart >= assignmentOneStart
            and assignmentTwoStart <= assignmentOneEnd
        )
        or (
            assignmentTwoEnd <= assignmentOneEnd
            and assignmentTwoEnd >= assignmentOneStart
        )
    ):
        return True
    return False


dataPath = Path(__file__).with_name("Data.txt")
with open(dataPath) as dataFile:
    assignmentLines = [getAssignments(line) for line in dataFile]
    fullyOverlappingAssignments = list(filter(isFullyOverlapping, assignmentLines))
    print(
        f"Number of fully overlapping assignments: {len(fullyOverlappingAssignments)}"
    )
    overlappingAssignments = list(filter(isOverlapping, assignmentLines))
    print(f"Number of partially overlapping assignments: {len(overlappingAssignments)}")
