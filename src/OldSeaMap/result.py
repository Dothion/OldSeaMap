# -*- coding: utf-8 -*-

# @File    : result.py
# @Date    : 2020-11-16
# @Author  : Dothion


from __future__ import annotations

from typing import Callable, Union

from .type_vars import _a
from .typeclasses import Monad

__all__ = ['Ok', 'Err']

_SometimesCallable = Union[Callable, _a]


class Result(Monad[_a]):
    ...


class Ok(Result[_a]):
    ...


class Err(Result[_a]):
    ...
