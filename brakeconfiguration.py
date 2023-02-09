import obd, threading, time

from obd2reader import OBD2Reader
from enum import Enum
from collections import OrderedDict
from datetime import datetime

class BrakeState(Enum):
    WAIT_FOR_TARGET_SPEED = 1
    TARGET_SPEED_REACHED = 2
    VEHICLE_STOPPED = 3
    FINISHED = 4

class BrakeConfiguration(threading.Thread):
    TARGET_KMH = 30.0

    def __init__(self) -> None:
        threading.Thread.__init__(self, daemon=True)
        self._obd = OBD2Reader()
        self._mp = OrderedDict()
        self._state = BrakeState.WAIT_FOR_TARGET_SPEED

    def run(self) -> None:
        self._obd.watch(obd.commands.SPEED, callback=self._newMp)
        self._obd.start()
        while True:
            time.sleep(0.1)
            if self._state == BrakeState.FINISHED:
                return

    def _newMp(self, data: obd.OBDResponse) -> None:
        if data.value == None:
            return
        saveValue = False
        kmh = data.value.magnitude
        ms = round(data.value / 3.6, 2)
        print(kmh)
        if (self._state == BrakeState.WAIT_FOR_TARGET_SPEED):
            if (kmh >= BrakeConfiguration.TARGET_KMH):
                # play sound
                saveValue = True
                self._state = BrakeState.TARGET_SPEED_REACHED
                print("TARGET SPEED REACHED")
        if (self._state == BrakeState.TARGET_SPEED_REACHED):
            saveValue = True
            if (kmh == 0):
                self._state = BrakeState.VEHICLE_STOPPED
                print("VEHICLE STOPPED")
        if (self._state == BrakeState.VEHICLE_STOPPED):
            #self._stop()
            self._analyzeResults()
            self._state = BrakeState.FINISHED

        if (saveValue):
            self._mp[datetime.now()] = ms

    def _stop(self) -> None:
        self._obd.stop()
        self._obd.unwatch(obd.commands.SPEED, self._newMp)

    def _analyzeResults(self) -> None:
        print("analyze")
        startTime = None
        startV = None
        print(len(self._mp.items()))
        for timestamp, value in self._mp.items():
            value = value.magnitude
            if (value * 3.6) < self.TARGET_KMH:
                startTime = timestamp
                startV = value
                break
        assert (startTime and startV)
        endTime = list(self._mp.keys())[-1]
        deacceleration = startV / (endTime - startTime).seconds
        print("DEACCELERATION: ", deacceleration)
