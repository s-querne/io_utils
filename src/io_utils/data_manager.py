from collections import abc
import logging
from pathlib import Path
import typing as t

from io_utils.utils import validate_path

T = t.TypeVar('T')
class DataManager(t.Generic[T]):
    def __init__(self, reader: abc.Callable[[Path], T]):
        self._reader = reader

    def read_file(self, path: Path, /):
        try:
            return self._reader(path)
        except Exception as e:
            logging.error(f"failed to read file {path}:\n{e}")

    def stream_files_from_iterable(
        self, paths: abc.Iterable[Path],
    ):
        for p in paths:
            if (value := self.read_file(p)) is not None:
                yield p, value

    def stream_files_from_dir(
        self,
        root_dir: Path, /,
        filter_func: abc.Callable[[Path], bool] | None = None,
    ):
        validate_path(root_dir, isdir=True)
        if filter_func is None:
            return self.stream_files_from_iterable(root_dir.iterdir())
        return self.stream_files_from_iterable(
            paths=filter(filter_func, root_dir.iterdir())
        )
