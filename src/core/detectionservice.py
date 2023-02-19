from definitions import ROOT_DIR, REACTION_TIME, BUFFER_DIST

from .tf03reader import TF03Reader
from .obd2reader import OBD2Reader
from .soundplayer import SoundPlayer

class DetectionService:
    def __init__(self, tf03: TF03Reader, obd2: OBD2Reader) -> None:
        self._tf03 = tf03
        self._obd = obd2
        self._player = SoundPlayer(f"{ROOT_DIR}/assets/warning_sound.wav")
        self._tf03.setCallback(self._distanceUpdate)
        self._obd.watchSpeed(self._speedUpdate)
        self._lastSpeed = 0
        self._lastDist = 0
        self._threads = [self._tf03, self._obd, self._player]
 
    def start(self) -> None:
        for th in self._threads:
            th.start()
        for th in self._threads:
            th.join()
 
    def _distanceUpdate(self, dist: int) -> None:
        self._lastDist = dist
        self._updateReactionPath()
 
    def _speedUpdate(self, kph: int) -> None:
        self._lastSpeed = round(kph / 3.6, 2) # ms
        self._updateReactionPath()

    def _updateReactionPath(self) -> None:
        self._player.setPlayWarning(self._lastDist != 0 and (self._lastSpeed * REACTION_TIME / 1000) > (self._lastDist + BUFFER_DIST) / 100)
