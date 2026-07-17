from pathlib import Path

from dotenv import dotenv_values

from io_utils.utils import validate_path

class DotenvLoader:
    def __init__(self, dotenv_path: Path | None = None):
        self.dotenv_path = dotenv_path or Path(".env")
        self.config = dotenv_values(self.dotenv_path)

    def load_path_var(
        self, var_name: str, /, isdir: bool = False, default: Path | None = None
    ):
        value = self.config.get(var_name, None)
        if value is None:
            if default is None:
                raise KeyError(
                    f"missing key '{var_name}' in dotenv file:\n{self.dotenv_path}"
                )
            result = default
        else:
            result = Path(value)
        validate_path(result, isdir=isdir)
        return result
