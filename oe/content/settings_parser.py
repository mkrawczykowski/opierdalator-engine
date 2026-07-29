"""
Parser pliku settings.md.

Obsługiwany format:
    no_of_layouts: 4
    variability: 10%
"""

import pathlib
from dataclasses import dataclass


@dataclass
class Settings:
    no_of_layouts: int
    variability_pct: float  # wartość 0.0–100.0


_DEFAULTS = Settings(no_of_layouts=1, variability_pct=0.0)


def parse_settings(settings_path: pathlib.Path) -> Settings:
    """
    Wejście:  ścieżka do settings.md
    Wyjście:  Settings

    Brakujące klucze uzupełniane są wartościami domyślnymi.
    """
    if not settings_path.exists():
        return _DEFAULTS

    params: dict[str, str] = {}

    for line in settings_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or ":" not in stripped:
            continue
        key, _, value = stripped.partition(":")
        params[key.strip()] = value.strip()

    no_of_layouts = _to_int(params.get("no_of_layouts"), _DEFAULTS.no_of_layouts)
    variability_pct = _to_float_pct(params.get("variability"), _DEFAULTS.variability_pct)

    return Settings(
        no_of_layouts=max(1, no_of_layouts),
        variability_pct=max(0.0, min(100.0, variability_pct)),
    )


def _to_int(value: str | None, default: int) -> int:
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def _to_float_pct(value: str | None, default: float) -> float:
    if value is None:
        return default
    try:
        return float(value.rstrip("%"))
    except ValueError:
        return default
