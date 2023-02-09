from .tf03reader import TF03Reader
from .obd2reader import OBD2Reader

class DetectionService:
    def __init__(self, tf03: TF03Reader, obd2: OBD2Reader) -> None:
        self._tf03 = tf03
        self._obd = obd2
        self._tf03.setCallback(self._distanceUpdate)
        self._obd.watchSpeed(self._speedUpdate)
        self._threads = [self._tf03, self._obd]

    def start(self) -> None:
        for th in self._threads:
            th.start()
        for th in self._threads:
            th.join()

    def _distanceUpdate(self, dist: int) -> None:
        print(f"New dist: {dist}")

    def _speedUpdate(self, kph: int) -> None:
        ms = round(kph / 3.6, 2)
        print(f"New speed {ms}")
