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
                if item < comparisonPacket:
                    return True
                elif item > comparisonPacket:
                    return False
            elif isinstance(comparisonPacket, list):
                if not checkPacketOrder([item], comparisonPacket):
                    return False
        if isinstance(item, list):
            if isinstance(comparisonPacket, int):
                if not checkPacketOrder(item, [comparisonPacket]):
                    return False
            elif isinstance(comparisonPacket, list):
                if not checkPacketOrder(item, comparisonPacket):
                    return False
    if len(rightPacket) < len(leftPacket):
        return False
    return True


def comparePackets(
    leftPackets: list[PacketType], rightPackets: list[PacketType]
) -> Generator[int, None, None]:
    for index, packet in enumerate(leftPackets):
        if checkPacketOrder(packet, rightPackets[index]):
            yield index + 1


def main() -> None:
    dataPath = Path(__file__).with_name("ExtraTest.txt")
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
        # 690 too low


main()
