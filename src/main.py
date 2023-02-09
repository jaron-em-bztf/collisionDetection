#!/usr/bin/env python3

import threading, time
from core import TF03Reader, OBD2Reader

class Printer(threading.Thread):
    def __init__(self, tf03):
        super().__init__(daemon=True)
        self._tf03 = tf03
        self._exitFlag = False

    def exit(self):
        self._exitFlag = True

    def run(self):
        while True:
            time.sleep(1)
            print(f"{self._tf03.distance()}")


def main():
    # '.\\COM7'
    tf03 = TF03Reader('COM14', 115200)
    printer = Printer(tf03)
    tf03.start()
    printer.start()
    tf03.join()
    #while True: time.sleep(100)
    #bc = BrakeConfiguration()
    #bc.start()
    #bc.join()
    
if __name__ == "__main__":
    main()
