from abc import ABC, abstractmethod
from pathlib import Path
import typing as t

T = t.TypeVar("T")
class IDatumIO(ABC, t.Generic[T]):
    @abstractmethod
    def load(self, path: Path) -> T:...

    @abstractmethod
    def safe_load(self, path: Path) -> T:...

    @abstractmethod
    def dump(self, datum: T, path: Path) -> None:...
