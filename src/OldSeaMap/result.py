# -*- coding: utf-8 -*-

# @File    : result.py
# @Date    : 2020-11-16
# @Author  : Dothion


from __future__ import annotations

from typing import Callable, Union

from funcy import curry
# noinspection PyProtectedMember
from pampy import match

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

    def __eq__(self, other):
        """
        Eq a => Eq (Maybe a)
            equals (Ok a)  (Ok b)  = equals a b
            equals (Err a) (Err b) = equals a b
            equals _       _       = False
        """
        return match((self, other),
                     (Err, Ok), False,
                     (Ok, Err), False,
                     (Ok, Ok), lambda x, y: x.value == y.value,
                     (Err, Err), lambda x, y: x.errmsg == y.errmsg)

    def __gt__(self, other):
        """
        Ord a => Ord (Maybe a)
            gt (Ok a)  (Ok b)  = gt a b
            gt _       (Err a) = error
            gt (Err a) _       = error
        """
        return match((self, other),
                     (Ok, Ok), lambda x, y: x.value > y.value)

    def __hash__(self):  # return match(self,
        #              Err, hash((Err, 'Err')),
        #              Ok, hash((Ok, self.value)))
        if isinstance(self, Ok):
            return hash((Ok, 'Ok', self.value))
        elif isinstance(self, Err):
            return hash((Err, 'Err', self.errmsg))

    def __repr__(self):
        # return match(self,
        #              Err, '<Err>',
        #              Ok, lambda x: f'<Ok {self.value}>')
        if isinstance(self, Ok):
            return f'<Ok {self.value}>'
        elif isinstance(self, Err):
            return f'<Err {self.errmsg}>'

    def __str__(self):
        # return match(self,
        #              Err, '<Err>',
        #              Ok, lambda x: f'<Ok {self.value}>')
        if isinstance(self, Ok):
            return f'{str(self.value)}'
        elif isinstance(self, Err):
            return f'<Err {self.errmsg}>'


class Ok(Result[_a]):
    def __init__(self, something):
        self._value = something if not isinstance(something, Callable) else curry(something)

    @property
    def value(self):
        return self._value

    def bind(self: Ok[_a], func: Callable[[_a], Result[_b]]) -> Result[_b]:
        try:
            return func(self.value)
        except Exception as e:
            return Err(str(e))


class Err(Result[_a]):
    def __init__(self, errmsg: str):
        self._errmsg = errmsg

    def bind(self: Err[_a], func: Callable[[_a], Result[_b]]) -> Err[_a]:
        return self

    @property
    def errmsg(self):
        return self._errmsg
