from io import TextIOWrapper
from pathlib import Path


def getValves(file: TextIOWrapper):
    fullFile = file.read()


def main() -> None:
    dataPath = Path(__file__).with_name("Data.txt")
    with open(dataPath) as dataFile:
        valveNetwork = getValves(dataFile)


main()
