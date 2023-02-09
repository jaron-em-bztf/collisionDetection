import obd

from obd import OBDCommand

from tf03reader import TF03Reader
from obd2reader import OBD2Reader

class DetectionService:
    def __init__(self, tf03Port: str, obdPort: str) -> None:
        self._tf03 = TF03Reader(tf03Port, 115200, self._distanceUpdate)
        self._obd = OBD2Reader(obdPort)
        self._obd.watch(obd.commands.SPEED, self._speedUpdate)
        self._treads = [self._tf03, self._obd]

    def start(self) -> None:
        for th in self._threads:
            th.start()
            th.join()

    def _distanceUpdate(self, dist: int) -> None:
        pass

    def _speedUpdate(self, data: obd.OBDResponse) -> None:
        kmh = data.value.magnitude
        ms = round(data.value / 3.6, 2)
