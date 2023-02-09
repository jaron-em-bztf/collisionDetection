import obd
from obd import OBDCommand
from typing import Callable

class OBD2Reader:
    def __init__(self, port: str):
        self._conn = obd.Async(portstr=port, delay_cmds=0.1)

    def start(self) -> None:
        self._conn.start()

    def stop(self) -> None:
        self._conn.stop()

    def watch(self, cmd: OBDCommand , callback: Callable[[int], None]) -> None:
        self._conn.watch(cmd, callback)
        # TODO watchSpeed method, return int

    def unwatch(self, cmd: OBDCommand, callback: Callable[[int], None]) -> None:
        self._conn.unwatch(cmd, callback)