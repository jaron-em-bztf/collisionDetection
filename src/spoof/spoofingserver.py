import threading

from flask import Flask
from typing import Dict

from spoof import OBD2Spoofer, TF03Spoofer

# misusing the Flask framework...
class SpoofingServer(threading.Thread):
    app = None

    def __init__(self, port: int, obd: OBD2Spoofer, tf03: TF03Spoofer) -> None:
        threading.Thread.__init__(self, daemon=True)
        self.port = port
        self._obd = obd
        self._tf03 = tf03
        self.app = Flask(__name__)
        self.app.add_url_rule("/speed/<float:kph>", view_func=self.setSpeed, methods=["PUT"])
        self.app.add_url_rule("/distance/<int:cm>", view_func=self.setDistance, methods=["PUT"])

    def run(self) -> None:
        self.app.run(port=self.port)

    def setSpeed(self, kph: float) -> Dict:
        self._obd.setCurrentKph(kph)
        return {"status": "OK"}
    
    def setDistance(self, cm: int) -> Dict:
        self._tf03.setDistance(cm)
        return {"status": "OK"}

