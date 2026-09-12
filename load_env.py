"""`.env`를 os.environ에 올리는 최소 로더. python-dotenv 없이 표준 라이브러리만 사용."""
from __future__ import annotations

from pathlib import Path


def load_env(path: str | Path = ".env") -> None:
    import os

    p = Path(path)
    if not p.exists():
        return
    for line in p.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())
