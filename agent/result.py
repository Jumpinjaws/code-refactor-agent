from typing import TypeVar, Generic, Union
from dataclasses import dataclass

T = TypeVar("T")
E = TypeVar("E")


@dataclass(frozen=True)
class Ok(Generic[T]):
    value: T
    ok: bool = True


@dataclass(frozen=True)
class Err(Generic[E]):
    error: E
    ok: bool = False


Result = Union[Ok[T], Err[E]]


def ok(value: T) -> Ok[T]:
    return Ok(value=value)


def err(error: E) -> Err[E]:
    return Err(error=error)


def is_ok(result: Result) -> bool:
    return result.ok


def unwrap(result: Result[T, E]) -> T:
    if not result.ok:
        raise ValueError(f"Called unwrap on Err: {result.error}")
    return result.value
