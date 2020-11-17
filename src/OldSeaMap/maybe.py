# -*- coding: utf-8 -*-

# @File    : maybe.py
# @Date    : 2020-11-16
# @Author  : Dothion

from __future__ import annotations

from abc import ABCMeta
from typing import Callable, Union

from funcy import curry
# noinspection PyProtectedMember
from pampy import match, _

from .type_vars import _a, _b
from .typeclasses import Monoid, Monad

__all__ = ['Just', 'NOTHING']

_PossiblyMonoid = Union[Monoid[_a], _a]
_SometimesCallable = Union[Callable, _a]


class Maybe(Monad[_a], Monoid[_a], metaclass=ABCMeta):
    @classmethod
    def of(cls, something: _SometimesCallable[_a]) -> Maybe[_SometimesCallable[_a]]:
        return Just(something)

    @classmethod
    def empty(cls) -> Maybe[_a]:
        return Nothing()

    def __eq__(self, other):
        """
        Eq a => Eq (Maybe a)
            equals (Just a) (Just b) = equals a b
            equals Nothing  Nothing  = True
            equals _        _        = False
        """
        return match((self, other),
                     (Nothing, Nothing), True,
                     (Just, Just), lambda x, y: x.value == y.value,
                     _, False)

    def __gt__(self, other):
        """
        Ord a => Ord (Maybe a)
            gt (Just a) (Just b) = gt a b
            gt (Just a) Nothing  = True
            gt Nothing  (Just a) = False
            gt Nothing  Nothing  = False
        """
        return match((self, other),
                     (Nothing, Nothing), False,
                     (Nothing, Just), False,
                     (Just, Nothing), True,
                     (Just, Just), lambda x, y: x.value > y.value)

    def __hash__(self):  # return match(self,
        #              Nothing, hash((Nothing, 'NOTHING')),
        #              Just, hash((Just, self.value)))
        if isinstance(self, Just):
            return hash((Just, 'Just', self.value))
        else:
            return hash((Nothing, 'NOTHING'))

    def __repr__(self):
        # return match(self,
        #              Nothing, '<Nothing>',
        #              Just, lambda x: f'<Just {self.value}>')
        if isinstance(self, Just):
            return f'<Just {self.value}>'
        else:
            return '<Nothing>'

    def __str__(self):
        # return match(self,
        #              Nothing, '<Nothing>',
        #              Just, lambda x: f'<Just {self.value}>')
        if isinstance(self, Just):
            return f'{str(self.value)}'
        else:
            return 'Nothing'


class Just(Maybe[_a]):
    def __init__(self: Just[_a], something: _a):
        self._value = something if not isinstance(something, Callable) else curry(something)

    @property
    def value(self: Just[_a]) -> _a:
        return self._value

    def append(self: Just[_PossiblyMonoid[_a]], other: Maybe[_PossiblyMonoid[_a]]) -> Just[_PossiblyMonoid[_a]]:
        if isinstance(other, Nothing):
            return self
        elif isinstance(other, Just):
            return Just(self.value.append(other.value))
        raise ValueError

    def bind(self: Just[_a], func: Callable[[_a], Monad[_b]]) -> Monad[_b]:
        return func(self.value)


class Nothing(Maybe[_a]):
    def append(self: Nothing, other: Maybe[_PossiblyMonoid[_a]]) -> Maybe[_PossiblyMonoid[_a]]:
        return other

    def bind(self: Nothing, func: Callable[[_a], Monad[_b]]) -> Monad[_b]:
        return self


NOTHING = Nothing()
