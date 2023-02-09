import serial, threading
from typing import Callable

class TF03Reader(threading.Thread):
    def __init__(self, interface: str, baud: int) -> None:
        super().__init__(daemon=True)
        self.interface = interface
        self.baud = baud
        self._lock = threading.Lock()
        self._serial = None
        self._distance = None
        self._exitFlag = False
        self._cb = None

    def setCallback(self, cb: Callable[[int], None]) -> None:
        self._cb = cb

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
        while True:
            if self._serial.in_waiting > 8:
                bytes = self._serial.read(9)
                self._serial.reset_input_buffer()
                # Frame header: 2x 0x59 byte
                if bytes[0] == 0x59 and bytes[1] == 0x59:
                    self._lock.acquire()
                    # Byte 2: distance low, Byte 3: distance high
                    dist = bytes[2] + bytes[3]*256
                    # 180m means error
                    if dist != 18000: 
                        self._distance = dist  
                    self._lock.release()
                    if self._cb != None:
                        self._cb(dist)
                    self._serial.reset_input_buffer()
