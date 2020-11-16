# -*- coding: utf-8 -*-

# @File    : typeclasses.py
# @Date    : 2020-11-16
# @Author  : Dothion

from __future__ import annotations

from typing import Callable, Protocol, runtime_checkable

from .type_vars import _a, _b


@runtime_checkable
class Functor(Protocol[_a]):
    def map(self: Functor[_a], func: Callable[[_a], _b]) -> Functor[_b]:
        raise NotImplementedError


@runtime_checkable
class Monoid(Protocol[_a]):
    @classmethod
    def empty(cls) -> Monoid[_a]:
        raise NotImplementedError

    def append(self: Monoid[_a], other: _a) -> Monoid[_a]:
        raise NotImplementedError


@runtime_checkable
class Applicative(Functor[_a]):
    def ap(self: Applicative[_a], other: Applicative[Callable[[_a], _b]]) -> Applicative[_b]:
        raise NotImplementedError

    @classmethod
    def of(cls, func: Callable[[_a], _b]) -> Applicative[Callable[[_a], _b]]:
        raise NotImplementedError

    def map(self: Applicative[_a], func: Callable[[_a], _b]) -> Applicative[_b]:
        return self.ap(self.of(func))


@runtime_checkable
class Monad(Applicative[_a]):
    def bind(self: Monad[_a], action: Callable[[_a], Monad[_b]]) -> Monad[_b]:
        raise NotImplementedError

    @classmethod
    def of(cls, func: Callable[[_a], _b]) -> Monad[Callable[[_a], _b]]:
        raise NotImplementedError

    def ap(self: Monad[_a], other: Monad[Callable[[_a], _b]]) -> Monad[_b]:
        return self.bind(lambda x: other.bind(lambda y: self.of(x(y))))