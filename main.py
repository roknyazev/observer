import dataclasses
import typing
from enum import Flag, auto, Enum
from functools import wraps
from glob import glob
from pathlib import *


class EventType(Flag):
    create = auto()
    delete = auto()


@dataclasses.dataclass
class Event:
    type: EventType
    payload: str


class PollingObserver:
    def __init__(self):
        self._listeners: list[typing.Callable[[Event], None]] = []

    def listener(self, callback: typing.Callable[[Event], None]) -> None:
        self._listeners.append(callback)

    def emit(self, event: Event):
        for listener in self._listeners:
            listener(event)


observer = PollingObserver()


@observer.listener
def test(event: Event):
    match event.type:
        case EventType.create:
            print('create', event.payload)
        case EventType.delete:
            print('delete', event.payload)


observer.emit(Event(type=EventType.delete, payload="vfdokjnffdjpf"))

print(glob(r'**/*', recursive=False, include_hidden=False))


print(list(Path().glob(r'*/*')))
