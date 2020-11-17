# -*- coding: utf-8 -*-

# @File    : typeclasses.py
# @Date    : 2020-11-16
# @Author  : Dothion

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Callable, Protocol, Union, runtime_checkable

from funcy import curry

from .type_vars import _a, _b

_SometimesCallable = Union[Callable, _a]


@runtime_checkable
class Functor(Protocol[_a], metaclass=ABCMeta):
    @abstractmethod
    def map(self: Functor[_a], func: Callable[[_a], _b]) -> Functor[_b]:
        ...

    def replace_with(self, something):
        return self.map(lambda x: something)


@runtime_checkable
class Monoid(Protocol[_a], metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def empty(cls) -> Monoid[_a]:
        ...

    @abstractmethod
    def append(self: Monoid[_a], other: _a) -> Monoid[_a]:
        ...


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


class Monad(Applicative[_a], metaclass=ABCMeta):
    @abstractmethod
    def bind(self: Monad[_a], func: Callable[[_a], Monad[_b]]) -> Monad[_b]:
        ...

    @classmethod
    @abstractmethod
    def of(cls, something: _SometimesCallable[_a]) -> Monad[_SometimesCallable[_a]]:
        ...

    def map(self: Monad[_a], func: Callable[[_a], _b]) -> Monad[_b]:
        return self.bind(lambda x: self.of(func(x)))

    def ap(self: Monad[_a], other: Monad[Callable[[_a], _b]]) -> Monad[_b]:
        return other.bind(lambda y: self.bind(lambda x: self.of(y(x))))
