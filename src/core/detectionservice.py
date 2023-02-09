from tf03reader import TF03Reader
from obd2reader import OBD2Reader

class DetectionService:
    def __init__(self, tf03Port: str, obdPort: str) -> None:
        self._tf03 = TF03Reader(tf03Port, 115200, self._distanceUpdate)
        self._obd = OBD2Reader(obdPort)

        self._obd.watchSpeed(self._speedUpdate)
        self._treads = [self._tf03, self._obd]

    def start(self) -> None:
        for th in self._threads:
            th.start()
            th.join()

    def _distanceUpdate(self, dist: int) -> None:
        pass

    def _speedUpdate(self, kph: int) -> None:
        ms = round(kph / 3.6, 2)
