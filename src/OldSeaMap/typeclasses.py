# -*- coding: utf-8 -*-

# @File    : typeclasses.py
# @Date    : 2020-11-16
# @Author  : Dothion

from __future__ import annotations

from typing import Callable, Protocol, Union, runtime_checkable

from .type_vars import _a, _b

_SometimesCallable = Union[Callable, _a]


@runtime_checkable
class Functor(Protocol[_a]):
    def map(self: Functor[_a], func: Callable[[_a], _b]) -> Functor[_b]:
        raise NotImplementedError

    def replace_with(self, something):
        return self.map(lambda x: something)


@runtime_checkable
class Monoid(Protocol[_a]):
    @classmethod
    def empty(cls) -> Monoid[_a]:
        raise NotImplementedError

    def append(self: Monoid[_a], other: _a) -> Monoid[_a]:
        raise NotImplementedError


class Applicative(Functor[_a]):
    def ap(self: Applicative[_a], other: Applicative[Callable[[_a], _b]]) -> Applicative[_b]:
        raise NotImplementedError

    @classmethod
    def of(cls, something: _SometimesCallable[_a]) -> Applicative[_a]:
        raise NotImplementedError

    def map(self: Applicative[_a], func: Callable[[_a], _b]) -> Applicative[_b]:
        return self.ap(self.of(func))


class Monad(Applicative[_a]):
    def bind(self: Monad[_a], func: Callable[[_a], Monad[_b]]) -> Monad[_b]:
        raise NotImplementedError

    @classmethod
    def of(cls, something: _SometimesCallable[_a]) -> Monad[_SometimesCallable[_a]]:
        raise NotImplementedError

    def map(self: Monad[_a], func: Callable[[_a], _b]) -> Monad[_b]:
        return self.bind(lambda x: self.of(func(x)))

    def ap(self: Monad[_a], other: Monad[Callable[[_a], _b]]) -> Monad[_b]:
        return other.bind(lambda y: self.bind(lambda x: self.of(y(x))))
