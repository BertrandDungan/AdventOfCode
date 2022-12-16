from pathlib import Path
from re import search


def performOperation(line: str) -> tuple[int, int]:
    command = search(r"(-?[0-9]+)", line)
    if command is None:
        return (1, 0)
    return (2, int(command[1]))


def main() -> None:
    dataPath = Path(__file__).with_name("Data.txt")
    with open(dataPath) as dataFile:
        valueRegister = 1
        signalRegister = 0
        specialCycles = [20, 60, 100, 140, 180, 220]
        lineBreaks = [39, 79, 119, 159, 199, 239]
        cycleCount = 0
        current_CRT_row: list[str] = []
        for line in dataFile:
            cycleIncrement, add_x_value = performOperation(line)
            newCycle = cycleCount + cycleIncrement
            for cycle in range(cycleCount, newCycle):
                cycleRemainder = cycle % 40
                if abs(cycleRemainder - valueRegister) < 2:
                    current_CRT_row.append("#")
                else:
                    current_CRT_row.append(".")
                if cycle in specialCycles:
                    signalRegister += valueRegister * cycle
                if cycle in lineBreaks:
                    print("".join(current_CRT_row))
                    current_CRT_row = []
            valueRegister += add_x_value
            cycleCount = newCycle
        print(f"Sum of signal strengths: {signalRegister}")


main()
