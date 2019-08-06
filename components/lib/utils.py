from pathlib import Path


def expand_path(path: str) -> str:
    return Path(path).expanduser().resolve().__str__()
