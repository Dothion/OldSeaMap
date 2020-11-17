# -*- coding: utf-8 -*-

# @File    : applicative.py
# @Date    : 2020-11-17
# @Author  : Dothion

from __future__ import annotations
from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Callable, Union

from funcy import curry

from .functor import Functor
from ..type_vars import _a, _b

_SometimesCallable = Union[Callable, _a]


class Applicative(Functor[_a], metaclass=ABCMeta):
    @abstractmethod
    def ap(self: Applicative[_a], other: Applicative[Callable[[_a], _b]]) -> Applicative[_b]:
        ...

    @classmethod
    @abstractmethod
    def of(cls, something: _SometimesCallable[_a]) -> Applicative[_a]:
        ...

    def ap_with(self, other):
        return other.ap(self)

    def map(self: Applicative[_a], func: Callable[[_a], _b]) -> Applicative[_b]:
        return self.ap(self.of(func))

    @classmethod
    def lift_a(cls, n):
        def _lift_an(c: cls, f, *args):
            f = c.of(f)
            for arg in args:
                f = f.ap_with(c.of(arg))
            return f

        if not isinstance(n, int):
            return cls.lift_a(1)(n)
        if n <= 0:
            raise ValueError
        return curry(_lift_an, n + 2)(cls)
