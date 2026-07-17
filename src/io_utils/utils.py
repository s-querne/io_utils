from collections import abc
from functools import wraps
import inspect
from pathlib import Path
import typing as t

PathLike = str | bytes | Path

def validate_path(path: PathLike, /, isdir: bool = False):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Path {path} does not exist.")
    if isdir and not path.is_dir():
        raise NotADirectoryError(f"Path {path} is not a directory.")
    if not isdir and not path.is_file():
        raise FileNotFoundError(f"Path {path} is not a file.")
    
P = t.ParamSpec('P')
R = t.TypeVar('R')
@t.overload
def path_validator(
    func: None = None, /,
    *args: str,
    **kwargs: bool,
) -> abc.Callable[[abc.Callable[P, R]], abc.Callable[P, R]]:...

@t.overload
def path_validator(
    func: abc.Callable[P, R], /,
    *args: str,
    **kwargs: bool,
) -> abc.Callable[P, R]:...

def path_validator(
    func: abc.Callable[P, R] | None = None, /,
    *args: str,
    **kwargs: bool,
):
    processed_args = { k: False for k in args }
    processed_args.update(kwargs)

    def decorator(func: abc.Callable[P, R]):
        sig = inspect.signature(func)
        
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            for k, isdir in processed_args.items():
                nullable_path = bound_args.arguments.get(k, None)
                if nullable_path is None:
                    continue
                if isinstance(nullable_path, abc.Iterable):
                    for path in nullable_path:
                        validate_path(path, isdir=isdir)
                    continue
                validate_path(nullable_path, isdir=isdir)
            return func(*args, **kwargs)

        return wrapper
    
    if func is not None:
        return decorator(func)
    return decorator
