"""
Parser plików .md dla Opierdalator Engine.

Obsługiwane sekcje:
    #color_palette  — zmienne kolorów ($nazwa: #hex)
    #typography     — parametry typografii (heading_1, text, button)
    #components     — parametry komponentów (button, section, row)
    #content        — deklaratywne drzewo komponentów (@@tag: wartość)

Format #content:
    @@section
    @@row [ratio] [gap%]           np. @@row 1/2 5%
    @@column [#kolor|$zmienna]     np. @@column $color_bg
    @@heading_1: Treść nagłówka
    @@text: Treść akapitu
    @@button: Etykieta przycisku

Zasady:
- @@section otwiera nową sekcję.
- @@row otwiera Row wewnątrz sekcji.
- @@column otwiera Column wewnątrz Row; opcjonalny kolor tła inline.
- Komponenty-liście trafiają do najgłębszego otwartego kontenera.
- Puste linie są ignorowane.
- Wartości zaczynające się od $ są referencjami do zmiennych z #color_palette.
"""

import math
import pathlib
from dataclasses import replace

from oe.design.tokens import DesignTokens, ButtonToken, TypographyToken, SectionToken, RowToken
from oe.renderer.components import Section, Text, Heading1, Button, Row, Column
from oe.renderer.components.component import Component


def parse(md_path: pathlib.Path, tokens: DesignTokens) -> list[Section]:
    resolved_tokens = parse_tokens(md_path, tokens)
    return build_sections(md_path, resolved_tokens)


def parse_tokens(md_path: pathlib.Path, tokens: DesignTokens) -> DesignTokens:
    """
    Wyjmuje z pliku MD tokeny i zwraca zaktualizowane DesignTokens
    bez budowania sekcji.
    """
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    colors = _parse_color_palette(lines)
    tokens = _apply_typography(lines, tokens)
    return _apply_components(lines, tokens, colors)


def build_sections(md_path: pathlib.Path, tokens: DesignTokens) -> list[Section]:
    """
    Buduje drzewo komponentów z sekcji #content używając przekazanych tokenów.
    Nie aplikuje ponownie ustawień z pliku MD.
    """
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    colors = _parse_color_palette(lines)
    content_lines = _extract_section_lines(lines, "#content")
    return _build_sections(content_lines, tokens, colors)


# ------------------------------------------------------------------
# Parsowanie #color_palette
# ------------------------------------------------------------------

def _parse_color_palette(lines: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    inside = False
    for line in lines:
        stripped = line.strip()
        if stripped == "#color_palette":
            inside = True
            continue
        if inside and stripped.startswith("#"):
            break
        if inside and stripped.startswith("$") and ":" in stripped:
            name, _, value = stripped[1:].partition(":")
            result[name.strip()] = value.strip()
    return result


# ------------------------------------------------------------------
# Parsowanie #typography
# ------------------------------------------------------------------

_TYPOGRAPHY_MAP: dict[str, str] = {
    "heading_1": "heading",
    "text":      "body",
    "button":    "button_text",
}


def _apply_typography(lines: list[str], tokens: DesignTokens) -> DesignTokens:
    typography_lines = _extract_section_lines(lines, "#typography")
    updated = tokens
    for block_name, token_field in _TYPOGRAPHY_MAP.items():
        params = _parse_component_block(typography_lines, block_name)
        if not params:
            continue
        current: TypographyToken = getattr(updated, token_field)
        updated = replace(updated, **{token_field: _build_typography_token(current, params)})
    return updated


def _build_typography_token(base: TypographyToken, params: dict[str, str]) -> TypographyToken:
    def to_float(value: str, default: float) -> float:
        try:
            return float(value)
        except ValueError:
            return default

    font_size = max(1, int(to_float(params.get("size", ""), float(base.font_size))))
    lh_raw = params.get("line_height", "")
    if lh_raw:
        line_height = max(1, math.floor(font_size * to_float(lh_raw, 1.0)))
    else:
        line_height = base.line_height
    return replace(base, font_size=font_size, line_height=line_height)


# ------------------------------------------------------------------
# Parsowanie #components
# ------------------------------------------------------------------

def _apply_components(
    lines: list[str],
    tokens: DesignTokens,
    colors: dict[str, str],
) -> DesignTokens:
    component_lines = _extract_section_lines(lines, "#components")

    button_params  = _parse_component_block(component_lines, "button")
    section_params = _parse_component_block(component_lines, "section")
    row_params     = _parse_component_block(component_lines, "row")

    updated = tokens
    if button_params:
        updated = replace(updated, button=_build_button_token(updated.button, button_params, colors))
    if section_params:
        updated = replace(updated, section=_build_section_token(updated.section, section_params, colors))
    if row_params:
        updated = replace(updated, row=_build_row_token(updated.row, row_params, colors))
    return updated


def _parse_component_block(lines: list[str], block_name: str) -> dict[str, str]:
    result: dict[str, str] = {}
    inside = False
    for line in lines:
        if not line:
            continue
        if ":" not in line:
            inside = (line == block_name)
            continue
        if inside:
            key, _, value = line.partition(":")
            result[key.strip()] = value.strip()
    return result


def _build_button_token(base: ButtonToken, params: dict[str, str], colors: dict[str, str]) -> ButtonToken:
    def resolve(v: str) -> str:
        return colors.get(v[1:], v) if v.startswith("$") else v

    def to_int(v: str, d: int) -> int:
        try:
            return int(v)
        except ValueError:
            return d

    return replace(
        base,
        background=resolve(params.get("background_color", base.background)),
        border_color=resolve(params.get("background_color", base.border_color)),
        padding_x=to_int(params.get("padding_horizontal", ""), base.padding_x),
        padding_y=to_int(params.get("padding_vertical",   ""), base.padding_y),
        radius=to_int(params.get("border_radius", ""), base.radius),
        border_width=to_int(params.get("border_width", ""), base.border_width),
    )


def _build_section_token(base: SectionToken, params: dict[str, str], colors: dict[str, str]) -> SectionToken:
    def resolve(v: str) -> str:
        return colors.get(v[1:], v) if v.startswith("$") else v

    return replace(base, background_color=resolve(params.get("background_color", base.background_color)))


def _build_row_token(base: RowToken, params: dict[str, str], colors: dict[str, str]) -> RowToken:
    def resolve(v: str) -> str:
        return colors.get(v[1:], v) if v.startswith("$") else v

    def to_int(v: str, d: int) -> int:
        try:
            return int(v)
        except ValueError:
            return d

    return replace(
        base,
        max_width=max(1, to_int(params.get("max_width", ""), base.max_width)),
        background_color=resolve(params.get("background_color", base.background_color)),
    )


# ------------------------------------------------------------------
# Parsowanie #content — helpery inline
# ------------------------------------------------------------------

def _extract_section_lines(lines: list[str], section: str) -> list[str]:
    """Zwraca linie należące do podanej sekcji najwyższego poziomu."""
    inside = False
    result: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped == section:
            inside = True
            continue
        if inside and stripped.startswith("#") and stripped != section:
            break
        if inside:
            result.append(stripped)
    return result


def _parse_row_params(line: str) -> tuple[tuple[int, int], float]:
    """
    @@row [ratio] [gap%]
    Przykład: @@row 1/2 5%  →  col_ratios=(1,2), col_gap_pct=5.0
    """
    parts = line.split()[1:]
    col_ratios: tuple[int, int] = (1, 1)
    col_gap_pct: float = 0.0
    for part in parts:
        if "/" in part:
            try:
                a, _, b = part.partition("/")
                col_ratios = (max(1, int(a)), max(1, int(b)))
            except ValueError:
                pass
        elif part.endswith("%"):
            try:
                col_gap_pct = max(0.0, min(50.0, float(part[:-1])))
            except ValueError:
                pass
    return col_ratios, col_gap_pct


def _parse_column_params(line: str, colors: dict[str, str]) -> str | None:
    """
    @@column [kolor]
    kolor — #hex lub $zmienna; brak → None (transparentny)
    """
    parts = line.split()[1:]
    if not parts:
        return None
    token = parts[0]
    if token.startswith("$"):
        return colors.get(token[1:], None)
    if token.startswith("#"):
        return token
    return None


# ------------------------------------------------------------------
# Budowanie drzewa komponentów
# ------------------------------------------------------------------

def _build_sections(lines: list[str], tokens: DesignTokens, colors: dict[str, str]) -> list[Section]:
    sections: list[Section] = []
    current_section_children: list[Component] | None = None
    current_row: Row | None = None
    current_column: Column | None = None

    def flush_column() -> None:
        nonlocal current_column
        if current_column is not None and current_row is not None:
            current_row.children.append(current_column)
            current_column = None

    def flush_row() -> None:
        nonlocal current_row
        flush_column()
        if current_row is not None and current_section_children is not None:
            current_section_children.append(current_row)
            current_row = None

    def flush_section() -> None:
        nonlocal current_section_children
        flush_row()
        if current_section_children is not None:
            sections.append(Section(
                background_color=tokens.section.background_color,
                children=current_section_children,
            ))
            current_section_children = None

    for line in lines:
        if not line:
            continue

        if line == "@@section":
            flush_section()
            current_section_children = []
            continue

        if line.startswith("@@row"):
            if current_section_children is None:
                continue
            flush_row()
            col_ratios, col_gap_pct = _parse_row_params(line)
            current_row = Row(
                max_width=tokens.row.max_width,
                background_color=tokens.row.background_color,
                col_ratios=col_ratios,
                col_gap_pct=col_gap_pct,
                children=[],
            )
            continue

        if line.startswith("@@column"):
            if current_row is None:
                continue
            flush_column()
            current_column = Column(
                background_color=_parse_column_params(line, colors),
                children=[],
            )
            continue

        if current_section_children is None:
            continue

        component = _parse_component(line, tokens)
        if component is None:
            continue

        if current_column is not None:
            current_column.children.append(component)
        elif current_row is not None:
            current_row.children.append(component)
        else:
            current_section_children.append(component)

    flush_section()
    return sections


def _parse_component(line: str, tokens: DesignTokens) -> Component | None:
    if not line.startswith("@@"):
        return None

    tag, _, value = line[2:].partition(":")
    tag = tag.strip()
    value = value.strip()

    if tag == "heading_1":
        return Heading1(text=value, token=tokens.heading)
    if tag == "text":
        return Text(text=value, token=tokens.body)
    if tag == "button":
        return Button(label=value, typography=tokens.button_text, style=tokens.button)
    return None
