from playsound import playsound

class SoundPlayer:
    def __init__(self, warningSoundFile: str) -> None:
        self._warningSoundFile = warningSoundFile

    def playWarning(self) -> None:
        self._play(self._warningSoundFile)

    def _play(self, file: str) -> None:
        playsound(file)
