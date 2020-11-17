# -*- coding: utf-8 -*-

# @File    : result.py
# @Date    : 2020-11-16
# @Author  : Dothion


from __future__ import annotations

from typing import Callable, Union

from funcy import curry

from .type_vars import _a, _b
from .typeclasses.monad import Monad

__all__ = ['Ok', 'Err']

_SometimesCallable = Union[Callable, _a]


class Result(Monad[_a]):
    def bind(self: Monad[_a], func: Callable[[_a], Monad[_b]]) -> Monad[_b]:
        raise NotImplementedError

    @classmethod
    def of(cls, something: _SometimesCallable[_a]) -> Result[_SometimesCallable[_a]]:
        return Ok(something)


class Ok(Result[_a]):
    def __init__(self, something):
        self._value = something if not isinstance(something, Callable) else curry(something)

    @property
    def value(self):
        return self._value

    def bind(self: Ok[_a], func: Callable[[_a], Result[_b]]) -> Monad[_b]:
        return func(self.value)


class Err(Result[_a]):
    def bind(self: Err[_a], func: Callable[[_a], Result[_b]]) -> Err[_a]:
        return self
