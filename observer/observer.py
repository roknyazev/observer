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

        self._prev_scan = initial_scan
        self._delay = delay
        self._executor = executor if executor else ThreadPoolExecutor()

        self.scan = scanner(root, depth)
        self._listener: Callable[[ScanDiff], None] = print
        self._is_listener_awaitable = False

    def listen(self, fn: Callable[[ScanDiff], None]):
        self._listener = fn
        self._is_listener_awaitable = inspect.iscoroutinefunction(fn)

    def observe(self):
        while True:
            scan = self.scan()
            res = diff(self._prev_scan, scan)
            self._prev_scan = scan
            self._listener(res)
            time.sleep(self._delay)

    async def observe_async(self):
        loop = asyncio.get_running_loop()

        while True:
            scan = await loop.run_in_executor(self._executor, self.scan)
            res = diff(self._prev_scan, scan)
            self._prev_scan = scan
            if self._is_listener_awaitable:
                await self._listener(res)
            else:
                self._listener(res)
            await asyncio.sleep(self._delay)
