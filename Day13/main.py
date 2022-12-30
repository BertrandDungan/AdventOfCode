from json import loads
from pathlib import Path
from typing import Generator, Optional, Union

PacketType = list[Union[int, None, "PacketType"]]


def checkPacketOrder(leftPacket: PacketType, rightPacket: PacketType) -> Optional[bool]:
    for index, item in enumerate(leftPacket):
        if len(rightPacket) < index + 1:
            return False
        comparisonPacket = rightPacket[index]
        if isinstance(item, int):
            if isinstance(comparisonPacket, int):
                if item != comparisonPacket:
                    return item < comparisonPacket
            elif isinstance(comparisonPacket, list):
                result = checkPacketOrder([item], comparisonPacket)
                if result is not None:
                    return result
        elif isinstance(item, list):
            if isinstance(comparisonPacket, int):
                result = checkPacketOrder(item, [comparisonPacket])
                if result is not None:
                    return result
            elif isinstance(comparisonPacket, list):
                result = checkPacketOrder(item, comparisonPacket)
                if result is not None:
                    return result
    if len(leftPacket) < len(rightPacket):
        return True
    return None


def comparePackets(
    leftPackets: list[PacketType], rightPackets: list[PacketType]
) -> Generator[int, None, None]:
    for index, packet in enumerate(leftPackets):
        result = checkPacketOrder(packet, rightPackets[index])
        if result or result is None:
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


main()
