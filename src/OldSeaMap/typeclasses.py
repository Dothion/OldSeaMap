# -*- coding: utf-8 -*-

# @File    : typeclasses.py
# @Date    : 2020-11-16
# @Author  : Dothion

from __future__ import annotations

from typing import Callable, Protocol

from .type_vars import _a, _b


class Functor(Protocol[_a]):
    def map(self: Functor[_a], fn: Callable[[_a], _b]) -> Functor[_b]:
        raise NotImplementedError


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
    def of(cls, fn: Callable[[_a], _b]) -> Applicative[Callable[[_a], _b]]:
        raise NotImplementedError

    def map(self: Applicative[_a], func: Callable[[_a], _b]) -> Applicative[_b]:
        return self.ap(self.of(func))


class Monad(Applicative[_a]):
    def bind(self: Monad[_a], action: Callable[[_a], Monad[_b]]) -> Monad[_b]:
        raise NotImplementedError

    @classmethod
    def of(cls, fn: Callable[[_a], _b]) -> Monad[Callable[[_a], _b]]:
        raise NotImplementedError

    def ap(self: Monad[_a], other: Monad[Callable[[_a], _b]]) -> Monad[_b]:
        raise NotImplementedError
