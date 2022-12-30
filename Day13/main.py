from functools import cmp_to_key
from json import loads
from pathlib import Path
from typing import Generator, Literal, Union

PacketType = list[Union[int, None, "PacketType"]]


def checkPacketOrder(
    leftPacket: PacketType, rightPacket: PacketType
) -> Union[Literal[1], Literal[-1], Literal[0]]:
    for index, item in enumerate(leftPacket):
        if len(rightPacket) < index + 1:
            return -1
        comparisonPacket = rightPacket[index]
        if isinstance(item, int):
            if isinstance(comparisonPacket, int):
                if item != comparisonPacket:
                    if item < comparisonPacket:
                        return 1
                    elif item > comparisonPacket:
                        return -1
            elif isinstance(comparisonPacket, list):
                result = checkPacketOrder([item], comparisonPacket)
                if result != 0:
                    return result
        elif isinstance(item, list):
            if isinstance(comparisonPacket, int):
                result = checkPacketOrder(item, [comparisonPacket])
                if result != 0:
                    return result
            elif isinstance(comparisonPacket, list):
                result = checkPacketOrder(item, comparisonPacket)
                if result != 0:
                    return result
    if len(leftPacket) < len(rightPacket):
        return 1
    return 0


def comparePackets(
    leftPackets: list[PacketType], rightPackets: list[PacketType]
) -> Generator[int, None, None]:
    for index, packet in enumerate(leftPackets):
        result = checkPacketOrder(packet, rightPackets[index])
        if result != -1:
            yield index + 1


def main() -> None:
    dataPath = Path(__file__).with_name("Data.txt")
    with open(dataPath) as dataFile:
        dataString = dataFile.readlines()
        leftPackets: list[PacketType] = [
            loads(line.strip()) for line in dataString[::3]
        ]
        rightPackets: list[PacketType] = [
            loads(line.strip()) for line in dataString[1::3]
        ]
        correctOrderIndexes = comparePackets(leftPackets, rightPackets)
        indexSum = sum(correctOrderIndexes)
        print(f"The sum of correct indexes is {indexSum}")
        DIVIDER_ONE: list[PacketType] = [[2]]
        DIVIDER_TWO: list[PacketType] = [[6]]
        allPackets = leftPackets + rightPackets + DIVIDER_ONE + DIVIDER_TWO
        allSortedPackets = sorted(
            allPackets, key=cmp_to_key(checkPacketOrder), reverse=True
        )
        indexesOfDividers = [
            index
            for (index, item) in enumerate(allSortedPackets)
            if item == DIVIDER_ONE[0] or item == DIVIDER_TWO[0]
        ]
        decoderKey = (indexesOfDividers[0] + 1) * (indexesOfDividers[1] + 1)
        print(f"The decoder key is {decoderKey}")


main()
