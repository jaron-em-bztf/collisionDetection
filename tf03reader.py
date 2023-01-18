import serial, threading
from enum import Enum

class ParseState(Enum):
    WAIT_FOR_NEXT_FRAME = 1
    READ_DIST_L = 2
    READ_DIST_H = 3

class TF03Reader(threading.Thread):
    def __init__(self, interface: str, baud: int) -> None:
        super().__init__(daemon=True)
        self.interface = interface
        self.baud = baud
        self._lock = threading.Lock()
        self._serial = None
        self._distance = None
        self._exitFlag = False

    def distance(self):
        self._lock.acquire()
        dist = self._distance
        self._lock.release()
        return dist

    def exit(self):
        self._lock.acquire()
        self._exitFlag = True
        self._lock.release()

    def run(self) -> None:
        self._serial = serial.Serial(self.interface, self.baud)
        headerByteCount = 0
        state = ParseState.WAIT_FOR_NEXT_FRAME
        while True:
            byte = self._serial.read(1)
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
                self._lock.acquire()
                self._distance = (distH << 8) + distL
                self._lock.release()
                state = ParseState.WAIT_FOR_NEXT_FRAME

            if self._exitFlag:
                return