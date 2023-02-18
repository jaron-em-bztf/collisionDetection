import threading

from playsound import playsound

class SoundPlayer (threading.Thread):
    def __init__(self, warningSoundFile: str) -> None:
        threading.Thread.__init__(self, daemon=True)
        self._lock = threading.Lock()
        self._isPlaying = False
        self._warningSoundFile = warningSoundFile

    def run(self) -> None:
        while True:
            if self._isPlaying:
                self._play(self._warningSoundFile)


    def setPlayWarning(self, warn: bool) -> None:
        if warn == self._isPlaying:
            return
        self._lock.acquire()
        self._isPlaying = warn
        self._lock.release()

    def _play(self, file: str) -> None:
        playsound(file)
