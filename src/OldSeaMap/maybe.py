# -*- coding: utf-8 -*-

# @File    : maybe.py
# @Date    : 2020-11-16
# @Author  : Dothion

from __future__ import annotations

from typing import Callable, Union, Literal, Hashable

from funcy import curry
# noinspection PyProtectedMember
from pampy import match, _

from .type_vars import _a, _b
from .typeclasses import Monoid, Monad

__all__ = ['Just', 'NOTHING']

_PossiblyMonoid = Union[Monoid[_a], _a]
_SometimesCallable = Union[Callable, _a]


class Maybe(Monad[_a], Monoid[_a]):
    @classmethod
    def of(cls, something: _SometimesCallable[_a],
           reserve: Literal['This', 'Other'] = 'This',
           monadic_error_handling: bool = True) -> Maybe[_SometimesCallable[_a]]:
        return Just(something)

    @classmethod
    def empty(cls) -> Maybe[_a]:
        return Nothing()

    def append(self: Maybe[_a], other: _a) -> Maybe[_a]:
        raise NotImplementedError

    def bind(self: Monad[_a], func: Callable[[_a], Monad[_b]]) -> Monad[_b]:
        raise NotImplementedError


class Just(Maybe[_a]):
    def __init__(self: Just[_a], something: _a,
                 reserve: Literal['This', 'Other'] = 'This',
                 monadic_error_handling: bool = True):
        self._value = something if not isinstance(something, Callable) else curry(something)
        self._reserve = reserve
        self._monadic_error_handling = monadic_error_handling

    @property
    def value(self: Just[_a]) -> _a:
        return self._value

    @property
    def reserve(self: Just[_a]) -> _a:
        return self._reserve

    # noinspection PyBroadException
    def map(self: Just[_a], func: Callable[[_a], _b]) -> Maybe[_b]:
        if self._monadic_error_handling:
            try:
                return Just(curry(func)(self.value))
            except Exception:
                return NOTHING
        else:
            return Just(curry(func)(self.value))

    def ap(self: Just[_a], other: Monad[Callable[[_a], _b]]) -> Monad[_b]:
        return match(other,
                     Nothing, NOTHING,
                     Just, lambda x: self.map(x.value))

    def append(self: Just[_PossiblyMonoid[_a]], other: Maybe[_PossiblyMonoid[_a]]) -> Just[_PossiblyMonoid[_a]]:
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

    def bind(self: Just[_a], func: Callable[[_a], Monad[_b]]) -> Monad[_b]:
        return func(self.value)

    def __eq__(self: Just[_a], other: Maybe[_a]):
        if isinstance(other, Just):
            return self.value == other.value
        return False

    def __hash__(self: Just[Hashable[_a]]):
        return hash((type(self), self._value))

    def __gt__(self, other):
        return match(other,
                     Nothing, True,
                     Just, lambda x: self.value > x.value,
                     _, NotImplemented)

    def __repr__(self):
        return f'<Just {self.value}>'


class Nothing(Maybe[_a]):
    def append(self: Nothing, other: Maybe[_PossiblyMonoid[_a]]) -> Maybe[_PossiblyMonoid[_a]]:
        return other

    def bind(self: Nothing, func: Callable[[_a], Monad[_b]]) -> Monad[_b]:
        return self

    def __eq__(self: Nothing, other: Maybe[_a]):
        return isinstance(other, Nothing)

    def __hash__(self):
        return hash(type(self))

    def __gt__(self, other):
        return match(other,
                     Just, False,
                     Nothing, False,
                     _, NotImplemented)

    def __repr__(self):
        return f'<Nothing>'


NOTHING = Nothing()
