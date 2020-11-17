# -*- coding: utf-8 -*-

# @File    : monad.py
# @Date    : 2020-11-17
# @Author  : Dothion

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Callable, Union

from .applicative import Applicative
from ..type_vars import _a, _b

_SometimesCallable = Union[Callable, _a]


class Monad(Applicative[_a], metaclass=ABCMeta):
    @abstractmethod
    def bind(self: Monad[_a], func: Callable[[_a], Monad[_b]]) -> Monad[_b]:
        ...

    @classmethod
    @abstractmethod
    def of(cls, something: _SometimesCallable[_a]) -> Monad[_SometimesCallable[_a]]:
        ...

    def map(self: Monad[_a], func: Callable[[_a], _b]) -> Monad[_b]:
        return self.bind(lambda x: self.of(func(x)))

    def ap(self: Monad[_a], other: Monad[Callable[[_a], _b]]) -> Monad[_b]:
        return other.bind(lambda y: self.bind(lambda x: self.of(y(x))))
