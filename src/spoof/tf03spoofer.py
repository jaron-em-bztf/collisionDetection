import threading, time

from typing import Callable

class TF03Spoofer(threading.Thread):
    def __init__(self) -> None:
        threading.Thread.__init__(self, daemon=True)
        self._cb = None
        self._distanceCm = 0

    def setCallback(self, cb: Callable[[int], None]) -> None:
        self._cb = cb

    def distance(self):
        return self._distanceCm

    def exit(self):
        pass

    def run(self) -> None:
        while True:
            if self._cb != None:
                self._cb(self._distanceCm)
            time.sleep(0.1)

    # Spoofing methods
    def setDistance(self, cm: int) -> None:
        self._distanceCm = cm
