# -*- coding: utf-8 -*-

# @File    : cont.py
# @Date    : 2020-11-20
# @Author  : Dothion

from __future__ import annotations

from typing import Callable, Union

from funcy import curry, identity

from .type_vars import _a, _b, _r
from .typeclasses.monad import Monad

_SometimesCallable = Union[Callable, _a]


class Cont(Monad[_a]):
    def __init__(self: Cont[_r, _a], something: _a):
        self._composing = lambda k: k(something if not isinstance(something, Callable) else curry(something))

    def run(self: Cont[_r, _a], k: Callable[[_a], _r]) -> _r:
        return self._composing(curry(k))

    def bind(self: Cont[_r, _a], func: Callable[[_a], Cont[_r, _b]]) -> Cont[_r, _b]:
        return Cont(lambda k: self.run(lambda a: func(a).run(k))).run(identity)

    @classmethod
    def of(cls, something: _SometimesCallable[_a]) -> Cont[_r, _SometimesCallable[_a]]:
        return Cont(something)

    @staticmethod
    def call_cc(func: Callable[[Callable[[_a], Cont[_r, _b]]], Cont[_r, _a]]) -> Cont[_r, _a]:
        return Cont(lambda c: curry(func)(lambda a: Cont(lambda _: c(a)).run(identity)).run(c))

    def __eq__(self: Cont[_r, _a], other: Cont[_r, _b]) -> bool:
        return self.run(identity) == other.run(identity)

    def __repr__(self):
        return f'<Cont {self.run(identity)}>'
