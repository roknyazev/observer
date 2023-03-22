import typing
from enum import Flag, auto
from functools import wraps


class Event(Flag):
    create = auto()
    delete = auto()


F = typing.TypeVar('F', bound=typing.Callable[[Event], None])


class Observer:
    def __init__(self):
        self._listeners: list[typing.Callable[[Event], None]] = []

    def listener(self, callback: F) -> None:
        self._listeners.append(callback)

    @property
    def on(self):
        def wrapper(callback: F):
            self._listeners.append(callback)
            return callback

        return wrapper


observer = Observer()


# @observer.listener
def test(tmp):
    return '123'

observer.listener(test)

@observer.on
def test2(tmp: list):
    return '123'
