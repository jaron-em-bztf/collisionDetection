import serial, time
from enum import Enum

class ParseState(Enum):
    WAIT_FOR_NEXT_FRAME = 1
    READ_DIST_L = 2
    READ_DIST_H = 3

class TF03Reader:
    def __init__(self, interface: str, baud: int) -> None:
        self.interface = interface
        self.baud = baud

    def run(self) -> None:
        self.serial = serial.Serial(self.interface, self.baud)
        headerByteCount = 0
        state = ParseState.WAIT_FOR_NEXT_FRAME
        while True:
            byte = self.serial.read(1)
            if byte == b'\x00':
                continue
            if state == ParseState.WAIT_FOR_NEXT_FRAME:
                if byte == b'Y':
                    headerByteCount += 1
                    if headerByteCount == 2:
                        state = ParseState.READ_DIST_L
                        headerByteCount = 0
                else:
                    headerByteCount = 0          
            elif state == ParseState.READ_DIST_L:
                distL = int.from_bytes(byte, 'little')
                state = ParseState.READ_DIST_H
            elif state == ParseState.READ_DIST_H:
                distH = int.from_bytes(byte, 'little')
                dist = (distH << 8) + distL
                print(dist)
                state = ParseState.WAIT_FOR_NEXT_FRAME