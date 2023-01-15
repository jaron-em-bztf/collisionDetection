#!/usr/bin/env python3

import asyncio
from tf03reader import TF03Reader

def main():
    tf03 = TF03Reader('COM12', 115200)
    tf03.run()
    #tfTask = await asyncio.create_task(tf03.run)
    
if __name__ == "__main__":
    main()
    #loop = asyncio.get_event_loop()
    #loop.create_task(main())
    #loop.run_forever()