from pathlib import Path


def searchForPacketMarker(packet: str, size: int) -> int:
    packetLength = len(packet)
    for index, _ in enumerate(packet):
        assert index < packetLength - (size - 1)
        packetGroup = set(packet[index : index + size])
        if len(packetGroup) > size - 1:
            return index + size
    raise Exception("No packet marker was found")


dataPath = Path(__file__).with_name("Data.txt")
with open(dataPath) as dataFile:
    packet = dataFile.readline()
    packetMarkerIndex = searchForPacketMarker(packet, 4)
    messageMarkerIndex = searchForPacketMarker(packet, 14)
    print(f"Packet marker was found at character: {packetMarkerIndex}")
    print(f"Message marker was found at character: {messageMarkerIndex}")
