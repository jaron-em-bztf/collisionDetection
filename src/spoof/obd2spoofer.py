import threading, time

from typing import Callable

class OBD2Spoofer (threading.Thread):
    Speed = "speed"

    def __init__(self):
        threading.Thread.__init__(self, daemon=True)
        self._currentKph = 0
        self._callbacks = {self.Speed : []}
        self._stopFlag = False
        pass

    def run(self) -> None:
        while True:
            if self._stopFlag:
                return
            for c in self._callbacks[self.Speed]:
                c(self._currentKph)
            time.sleep(0.25)

    def stop(self) -> None:
        self._stopFlag = True

    def watchSpeed(self, callback: Callable[[int], None]) -> None:
        self._callbacks[self.Speed].append(callback)

    def unwatchAll(self) -> None:
        for c in self._callbacks.values():
            c.clear()

    # Spoofing methods
    def setCurrentKph(self, kph: int) -> None:
        self._currentKph = kph
