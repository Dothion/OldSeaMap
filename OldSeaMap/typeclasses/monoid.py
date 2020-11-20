# -*- coding: utf-8 -*-

# @File    : monoid.py
# @Date    : 2020-11-17
# @Author  : Dothion

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Callable, Union, Protocol, runtime_checkable

from ..type_vars import _a

_SometimesCallable = Union[Callable, _a]


@runtime_checkable
class Monoid(Protocol[_a], metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def empty(cls) -> Monoid[_a]:
        ...

    @abstractmethod
    def append(self: Monoid[_a], other: _a) -> Monoid[_a]:
        ...
