from typing import Any, Callable, Generic, Hashable, Iterable, TypeVar, overload

_KT = TypeVar("_KT", bound=Hashable)
_VT = TypeVar("_VT")
_T = TypeVar("_T")

class LRU(Generic[_KT, _VT]):

    def __init__(
        self, size: int, callback: Callable[[_KT, _VT], Any] | None = ...
    ) -> None: ...
    def clear(self) -> None: ...

    @overload
    def get(self, key: _KT) -> _VT: ...

    @overload
    def get(self, key: _KT, instead: _VT | _T) -> _VT | _T: ...

    def get_size(self) -> int: ...
    def has_key(self, key: _KT) -> bool: ...
    def keys(self) -> list[_KT]: ...
    def values(self) -> list[_VT]: ...
    def items(self) -> list[tuple[_KT, _VT]]: ...
    def peek_first_item(self) -> tuple[_KT, _VT] | None: ...
    def peek_last_item(self) -> tuple[_KT, _VT] | None: ...
    @overload
    def pop(self, key: _KT) -> _VT: ...
    @overload
    def pop(self, key: _KT, default: _VT | _T) -> _VT | _T: ...
    def popitem(self, least_recent: bool = ...) -> tuple[_KT, _VT]: ...
    @overload
    def setdefault(self: LRU[_KT, _T | None], key: _KT) -> _T | None: ...
    @overload
    def setdefault(self, key: _KT, default: _VT) -> _VT: ...
    def set_callback(self, callback: Callable[[_KT, _VT], Any]) -> None: ...
    def set_size(self, size: int) -> None: ...
    @overload
    def update(self, __m: Iterable[tuple[_KT, _VT]], **kwargs: _VT) -> None: ...
    @overload
    def update(self, **kwargs: _VT) -> None: ...
    def __contains__(self, __o: Any) -> bool: ...
    def __delitem__(self, key: _KT) -> None: ...
    def __getitem__(self, item: _KT) -> _VT: ...
    def __len__(self) -> int: ...
    def __repr__(self) -> str: ...
    def __setitem__(self, key: _KT, value: _VT) -> None: ...
