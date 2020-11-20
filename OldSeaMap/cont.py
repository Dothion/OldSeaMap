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


def call_cc(fn: Callable[[Callable[[_a], Cont[_r, _b]]], Cont[_r, _a]]) -> Cont[_r, _a]:
    return Cont(lambda c: fn(lambda a: Cont(lambda _: c(a))).run(c))


class Cont(Monad[_a]):
    def __init__(self: Cont[_r, _a], something: _a):
        self._composing = curry(something) if isinstance(something, Callable) else something

    def run(self: Cont[_r, _a], k: Callable[[_a], _r]) -> _r:
        return self._composing(k)

    def bind(self: Cont[_r, _a], func: Callable[[_a], Cont[_r, _b]]) -> Cont[_r, _b]:
        return Cont(lambda k: self.run(lambda a: func(a).run(k)))

    @classmethod
    def of(cls, something: _SometimesCallable[_a]) -> Cont[_SometimesCallable[_a]]:
        return Cont(curry(lambda k: k(something)))

    def __repr__(self):
        return f'<Cont {self.run(identity)}>'

    def __eq__(self, other: Cont):
        return self.run(identity) == other.run(identity)

    call_cc = staticmethod(call_cc)
