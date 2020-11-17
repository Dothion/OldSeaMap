# -*- coding: utf-8 -*-

# @File    : result.py
# @Date    : 2020-11-16
# @Author  : Dothion


from __future__ import annotations

from typing import Callable, Union, Literal

from funcy import curry
from pampy import match, _

from .type_vars import _a, _b
from .typeclasses import Monoid, Monad

__all__ = ['Ok', 'Err']

_PossiblyMonoid = Union[Monoid[_a], _a]
_SometimesCallable = Union[Callable, _a]


class Result(Monad[_a]):
    @classmethod
    def of(cls, something: _SometimesCallable[_a]) -> Result[_SometimesCallable[_a]]:
        return Ok(something)

    def bind(self: Monad[_a], func: Callable[[_a], Monad[_b]]) -> Monad[_b]:
        raise NotImplementedError

    def __gt__(self, other):
        return match((self, other),
                     (Err, Ok), True,
                     (Ok, Ok), lambda a, b: a.value > b.value,
                     (Ok, Err), False,
                     (Err, Err), False,
                     _, NotImplemented)

    def __repr__(self):
        if isinstance(self, Ok):
            return f'<Ok {self.value}>'
        elif isinstance(self, Err):
            return f'<Err>'


class Ok(Result[_a]):
    def __init__(self: Ok[_a], something: _a,
                 reserve: Literal['This', 'Other'] = 'This',
                 monadic_error_handling: bool = True):
        self._value = something if not isinstance(something, Callable) else curry(something)
        self._reserve = reserve
        self._monadic_error_handling = monadic_error_handling

    @property
    def value(self: Ok[_a]) -> _a:
        return self._value

    @property
    def reserve(self: Ok[_a]) -> _a:
        return self._reserve

    # noinspection PyBroadException
    def map(self: Ok[_a], func: Callable[[_a], _b]) -> Result[_b]:
        if self._monadic_error_handling:
            try:
                return Ok(curry(func)(self.value))
            except Exception:
                return Err
        else:
            return Ok(curry(func)(self.value))

    def ap(self: Ok[_a], other: Monad[Callable[[_a], _b]]) -> Monad[_b]:
        return match(other,
                     Err, Err,
                     Ok, lambda x: self.map(x.value),
                     _, NotImplemented)

    def bind(self: Ok[_a], func: Callable[[_a], Monad[_b]]) -> Monad[_b]:
        return func(self.value)

    def __eq__(self: Ok[_a], other: Result[_a]):
        if isinstance(other, Ok):
            return self.value == other.value
        return False


class Err(Result[_a]):
    def bind(self: Err, func: Callable[[_a], Monad[_b]]) -> Monad[_b]:
        return self

    def __eq__(self: Err, other: Result[_a]):
        return isinstance(other, Err)
