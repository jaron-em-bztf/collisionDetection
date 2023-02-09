import obd
from typing import Callable

class OBD2Reader:
    def __init__(self, port: str):
        self._conn = obd.Async(portstr=port, delay_cmds=0.1)

    def start(self) -> None:
        self._conn.start()

    def stop(self) -> None:
        self._conn.stop()

    # returns kph
    def watchSpeed(self, callback: Callable[[int], None]) -> None:
        self._conn.watch(obd.commands.SPEED, lambda resp: callback(resp.value.to("kph").magnitude))

    def unwatchAll(self) -> None:
        self._conn.unwatch(obd.commands.SPEED)
