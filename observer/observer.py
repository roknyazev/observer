import inspect
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Callable
import asyncio

from .scanner import *


class Observer:
    def __init__(self,
                 root: str,
                 depth: int,
                 delay: float,

                 initial_scan: list[set[Path]] = None,
                 executor=None):

        self.prev_scan = initial_scan
        self.delay = delay
        self.executor = executor if executor else ThreadPoolExecutor()

        self.scan = scanner(root, depth)
        self.listener: Callable[[ScanDiff], None] = print
        self.is_listener_awaitable = False

    def listen(self, fn: Callable[[ScanDiff], None]):
        self.listener = fn
        self.is_listener_awaitable = inspect.iscoroutinefunction(fn)

    def observe(self):
        while True:
            scan = self.scan()
            res = diff(self.prev_scan, scan)
            self.prev_scan = scan
            self.listener(res)
            time.sleep(self.delay)

    async def observe_async(self):
        loop = asyncio.get_running_loop()

        while True:
            scan = await loop.run_in_executor(self.executor, self.scan)
            res = diff(self.prev_scan, scan)
            self.prev_scan = scan
            if self.is_listener_awaitable:
                await self.listener(res)  # fixme Cannot find reference 'await' in 'None'
            else:
                self.listener(res)
            await asyncio.sleep(self.delay)
