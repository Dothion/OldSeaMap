# -*- coding: utf-8 -*-

# @File    : functor.py
# @Date    : 2020-11-17
# @Author  : Dothion

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import runtime_checkable, Protocol, Callable

from ..type_vars import _a, _b


@runtime_checkable
class Functor(Protocol[_a], metaclass=ABCMeta):
    @abstractmethod
    def map(self: Functor[_a], func: Callable[[_a], _b]) -> Functor[_b]:
        ...

    def replace_with(self, something):
        return self.map(lambda x: something)
