#!/usr/bin/env python3

import threading, time
from tf03reader import TF03Reader

class Printer(threading.Thread):
    def __init__(self, tf03):
        super().__init__(daemon=True)
        self._tf03 = tf03
        self._exitFlag = False

    def exit(self):
        self._exitFlag = True

    def run(self):
        while True:
            print(self._tf03.distance)
            time.sleep(1)


def main():
    tf03 = TF03Reader('COM12', 115200)
    printer = Printer(tf03)
    tf03.start()
    printer.start()
    while True: time.sleep(100)
    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass