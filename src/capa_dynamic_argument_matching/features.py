from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class API:
    name: str


@dataclass(frozen=True)
class String:
    value: str


@dataclass(frozen=True)
class Number:
    value: int


@dataclass(frozen=True)
class Argument:
    arg_name: str
    value: Any

    @property
    def name(self) -> str:
        suffix = "string" if isinstance(self.value, str) else "number"
        return f"arg[{self.arg_name}].{suffix}"


@dataclass(frozen=True)
class ReturnValue:
    value: int

    @property
    def name(self) -> str:
        return "return-value"
