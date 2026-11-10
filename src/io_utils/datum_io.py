from abc import ABC, abstractmethod
from pathlib import Path

class IDatumIO[T](ABC):
    @abstractmethod
    def load(self, path: Path) -> T:...

    @abstractmethod
    def safe_load(self, path: Path) -> T:...

    @abstractmethod
    def dump(self, datum: T, path: Path) -> None:...
