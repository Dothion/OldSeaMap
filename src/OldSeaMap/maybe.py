# -*- coding: utf-8 -*-

# @File    : maybe.py
# @Date    : 2020-11-16
# @Author  : Dothion

from __future__ import annotations

from typing import Callable, Union, Literal

from pampy import match, _

from .type_vars import _a, _b
from .typeclasses import Monoid, Monad

PossiblyMonoid = Union[Monoid[_a], _a]


class Maybe(Monad[_a], Monoid[_a]):
    @classmethod
    def of(cls, func: Callable[[_a], _b]) -> Monad[Callable[[_a], _b]]:
        return Just.of(func)

    @classmethod
    def empty(cls) -> Monoid[_a]:
        return Nothing()

    def append(self: Monoid[_a], other: _a) -> Monoid[_a]:
        raise NotImplementedError

    def bind(self: Monad[_a], action: Callable[[_a], Monad[_b]]) -> Monad[_b]:
        raise NotImplementedError

    def __eq__(self, other):
        return match((self, other),
                     (Nothing, Nothing), True,
                     (Just, Just), lambda a, b: a.value == b.value,
                     _, False)

    def __gt__(self, other):
        return match((self, other),
                     (Nothing, Just), True,
                     (Just, Just), lambda a, b: a.value > b.value,
                     (Just, Nothing), False,
                     (Nothing, Nothing), False,
                     _, NotImplemented)

    def __str__(self):
        # return match(self,
        #              Nothing, 'Nothing',
        #              Just, f'Just<{self.value}>',
        #              _, NotImplemented)
        if isinstance(self, Just):
            return f'<Just {self.value}>'
        elif isinstance(self, Nothing):
            return f'<Nothing>'


class Just(Maybe[_a]):
    def __init__(self: Just[_a], value: _a, reserve: Literal['This', 'Other'] = 'This'):
        self._value = value
        self._reserve = reserve

    @property
    def value(self: Just[_a]) -> _a:
        return self._value

    @property
    def reserve(self: Just[_a]) -> _a:
        return self._reserve

    def append(self: Just[PossiblyMonoid[_a]], other: Maybe[PossiblyMonoid[_a]]) -> Just[PossiblyMonoid[_a]]:
        if isinstance(other, Nothing):
            return self
        elif isinstance(other, Just):
            if isinstance(self.value, Monoid):
                return self.value.append(other.value)
            elif self.reserve != other.reserve:
                raise ValueError
            else:
                return self if self.reserve == 'This' else other
        else:
            raise ValueError

    def bind(self: Just[_a], action: Callable[[_a], Monad[_b]]) -> Monad[_b]:
        return action(self.value)


class Nothing(Maybe[_a]):
    def append(self: Nothing, other: Maybe[PossiblyMonoid[_a]]) -> Maybe[PossiblyMonoid[_a]]:
        return other

    def bind(self: Monad[_a], action: Callable[[_a], Monad[_b]]) -> Monad[_b]:
        return self
