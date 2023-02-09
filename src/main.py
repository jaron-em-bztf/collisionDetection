#!/usr/bin/env python3

import sys

from core import TF03Reader, OBD2Reader, BrakeConfiguration, DetectionService
from spoof import OBD2Spoofer, TF03Spoofer, SpoofingServer

def brakeConfiguration() -> None:
    bc = BrakeConfiguration()
    bc.start()
    bc.join()

def main():
    tf03 = None
    obd2 = None

    if len(sys.argv) == 2:
        arg = sys.argv[1]
        if arg == "brakeconfiguration":
            brakeConfiguration()
            return
        elif arg == "test":
            tf03 = TF03Spoofer()
            obd2 = OBD2Spoofer()
            server = SpoofingServer(5000, obd2, tf03)
            server.start()
        else:
            print(f"Unknown argument {arg}")
            sys.exit(1)
        
    if tf03 == None and obd2 == None:
        tf03 = TF03Reader('COM14', 115200)
        obd2 = OBD2Reader('COM7')

    assert(tf03 != None and obd2 != None)
    service = DetectionService(tf03, obd2)
    service.start()

    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Shutdown")
        sys.exit(0)
