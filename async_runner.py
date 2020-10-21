import asyncio
from utils import file_buffer
import time


async def async_main():
    receiver = file_buffer()
    s = time.time()
    tasks = [receiver.send(f'test{i}') for i in range(100)]
    await asyncio.wait(tasks)
    print('end;', time.time() - s)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_main())