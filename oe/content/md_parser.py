"""
Parser plików .md dla Opierdalator Engine.

Obsługiwane sekcje:
    #color_palette  — zmienne kolorów ($nazwa: #hex)
    #typography     — parametry typografii (heading_1, text, button)
    #components     — parametry komponentów (button, section)
    #content        — deklaratywne drzewo komponentów (@@tag: wartość)

Format #content:
    @@section
    @@heading_1: Treść nagłówka
    @@text: Treść akapitu
    @@button: Etykieta przycisku

Zasady:
- @@section otwiera nową sekcję; komponenty trafiają do bieżącej sekcji.
- Komponenty przed pierwszym @@section są ignorowane.
- Puste linie są ignorowane.
- Linie poza obsługiwanymi sekcjami są ignorowane.
- Wartości zaczynające się od $ są referencjami do zmiennych z #color_palette.
"""

import math
import pathlib
from dataclasses import replace

from oe.design.tokens import DesignTokens, ButtonToken, TypographyToken, SectionToken, RowToken
from oe.renderer.components import Section, Text, Heading1, Button, Row, Column
from oe.renderer.components.component import Component


def parse(md_path: pathlib.Path, tokens: DesignTokens) -> list[Section]:
    """
    Wejście:  ścieżka do pliku .md, DesignTokens (wartości domyślne)
    Wyjście:  lista Section gotowa do przekazania do LayoutRenderer

    Tokeny z pliku MD nadpisują wartości domyślne tam, gdzie
    plik MD definiuje odpowiednie parametry.
    """
    resolved_tokens = parse_tokens(md_path, tokens)
    return build_sections(md_path, resolved_tokens)


def parse_tokens(md_path: pathlib.Path, tokens: DesignTokens) -> DesignTokens:
    """
    Wyjmuje z pliku MD tokeny (kolory, typografię, parametry komponentów)
    i zwraca zaktualizowane DesignTokens — bez budowania sekcji.

    Używane gdy caller chce zmodyfikować tokeny (np. przez TokenVariator)
    przed ostatecznym zbudowaniem drzewa komponentów.
    """
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    colors = _parse_color_palette(lines)
    tokens = _apply_typography(lines, tokens)
    return _apply_components(lines, tokens, colors)


def build_sections(md_path: pathlib.Path, tokens: DesignTokens) -> list[Section]:
    """
    Buduje drzewo komponentów z sekcji #content używając przekazanych tokenów.

    Nie aplikuje ponownie ustawień z pliku MD — tokeny są traktowane
    jako ostateczne. Dzięki temu variator może je zmodyfikować przed
    wywołaniem tej funkcji.
    """
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    content_lines = _extract_section_lines(lines, "#content")
    return _build_sections(content_lines, tokens)


# ------------------------------------------------------------------
# Parsowanie #color_palette
# ------------------------------------------------------------------

def _parse_color_palette(lines: list[str]) -> dict[str, str]:
    """
    Zwraca słownik {nazwa_zmiennej: wartość_hex}.
    Klucze są przechowywane bez znaku $, np. "color_main_accent".
    """
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

# Mapowanie nazw bloków z #typography na pola DesignTokens
_TYPOGRAPHY_MAP: dict[str, str] = {
    "heading_1": "heading",
    "text":      "body",
    "button":    "button_text",
}


def _apply_typography(lines: list[str], tokens: DesignTokens) -> DesignTokens:
    """
    Czyta sekcję #typography i zwraca nowe DesignTokens
    z nadpisanymi wartościami font_size i line_height.

    line_height w pliku MD jest mnożnikiem (np. 1.4), natomiast
    TypographyToken przechowuje go jako int (px).
    Przeliczenie: line_height_px = floor(font_size * multiplier).
    """
    typography_lines = _extract_section_lines(lines, "#typography")

    updated = tokens
    for block_name, token_field in _TYPOGRAPHY_MAP.items():
        params = _parse_component_block(typography_lines, block_name)
        if not params:
            continue
        current: TypographyToken = getattr(updated, token_field)
        new_token = _build_typography_token(current, params)
        updated = replace(updated, **{token_field: new_token})

    return updated


def _build_typography_token(
    base: TypographyToken,
    params: dict[str, str],
) -> TypographyToken:
    """
    Tworzy TypographyToken z nadpisanymi wartościami z pliku MD.

    Obsługiwane klucze z #typography -> <komponent>:
        size        — rozmiar fontu w px (int)
        line_height — mnożnik (float), przeliczany na px: floor(size * multiplier)
    """
    def to_float(value: str, default: float) -> float:
        try:
            return float(value)
        except ValueError:
            return default

    font_size = int(to_float(params.get("size", ""), float(base.font_size)))
    font_size = max(1, font_size)

    lh_raw = params.get("line_height", "")
    if lh_raw:
        lh_multiplier = to_float(lh_raw, 1.0)
        line_height = max(1, math.floor(font_size * lh_multiplier))
    else:
        line_height = base.line_height

    return replace(base, font_size=font_size, line_height=line_height)


# ------------------------------------------------------------------
# Parsowanie #components i aplikowanie do tokenów
# ------------------------------------------------------------------

def _apply_components(
    lines: list[str],
    tokens: DesignTokens,
    colors: dict[str, str],
) -> DesignTokens:
    """
    Czyta sekcję #components i zwraca nowe DesignTokens
    z nadpisanymi wartościami z pliku MD.

    Obsługuje: button, section.
    """
    component_lines = _extract_section_lines(lines, "#components")

    button_params = _parse_component_block(component_lines, "button")
    section_params = _parse_component_block(component_lines, "section")
    row_params = _parse_component_block(component_lines, "row")

    updated = tokens

    if button_params:
        updated = replace(updated, button=_build_button_token(updated.button, button_params, colors))

    if section_params:
        updated = replace(updated, section=_build_section_token(updated.section, section_params, colors))

    if row_params:
        updated = replace(updated, row=_build_row_token(updated.row, row_params, colors))

    return updated


def _parse_component_block(
    lines: list[str],
    block_name: str,
) -> dict[str, str]:
    """
    Zwraca parametry konkretnego bloku komponentu jako słownik.

    Blok identyfikowany jest przez linię równą block_name (bez wcięcia
    w oryginalnym pliku, ale po strip — bez dwukropka).
    Parametry to kolejne linie zawierające dwukropek, aż do
    następnej nazwy bloku lub końca listy.
    """
    result: dict[str, str] = {}
    inside = False

    for line in lines:
        if not line:
            continue

        if ":" not in line:
            # Linia bez dwukropka to nazwa bloku
            inside = (line == block_name)
            continue

        if inside:
            key, _, value = line.partition(":")
            result[key.strip()] = value.strip()

    return result


def _build_button_token(
    base: ButtonToken,
    params: dict[str, str],
    colors: dict[str, str],
) -> ButtonToken:
    """Tworzy ButtonToken przez nadpisanie wartości bazowych parametrami z pliku.

    Obsługiwane klucze z #components -> button:
        background_color   — kolor tła (hex lub $zmienna z #color_palette)
        padding_vertical   — padding_y w px
        padding_horizontal — padding_x w px
        border_radius      — zaokrąglenie rogów w px
        border_width       — grubość obramowania w px
    """

    def resolve(value: str) -> str:
        if value.startswith("$"):
            return colors.get(value[1:], value)
        return value

    def to_int(value: str, default: int) -> int:
        try:
            return int(value)
        except ValueError:
            return default

    background  = resolve(params.get("background_color", base.background))
    padding_y   = to_int(params.get("padding_vertical",   ""), base.padding_y)
    padding_x   = to_int(params.get("padding_horizontal", ""), base.padding_x)
    radius      = to_int(params.get("border_radius",      ""), base.radius)
    border_width = to_int(params.get("border_width",      ""), base.border_width)

    return replace(
        base,
        background=background,
        border_color=background,
        padding_x=padding_x,
        padding_y=padding_y,
        radius=radius,
        border_width=border_width,
    )


def _build_section_token(
    base: SectionToken,
    params: dict[str, str],
    colors: dict[str, str],
) -> SectionToken:
    """Tworzy SectionToken z nadpisanymi wartościami z pliku MD.

    Obsługiwane klucze z #components -> section:
        background_color — kolor tła (hex lub $zmienna z #color_palette)
    """
    def resolve(value: str) -> str:
        if value.startswith("$"):
            return colors.get(value[1:], value)
        return value

    background_color = resolve(params.get("background_color", base.background_color))
    return replace(base, background_color=background_color)


def _build_row_token(base: RowToken, params: dict[str, str], colors: dict[str, str]) -> RowToken:
    """Tworzy RowToken z nadpisanymi wartościami z pliku MD.

    Obsługiwane klucze z #components -> row:
        max_width        — maksymalna szerokość contentu w px
        background_color — kolor tła (hex lub $zmienna z #color_palette)
    """
    def resolve(value: str) -> str:
        if value.startswith("$"):
            return colors.get(value[1:], value)
        return value

    def to_int(value: str, default: int) -> int:
        try:
            return int(value)
        except ValueError:
            return default

    max_width = to_int(params.get("max_width", ""), base.max_width)
    background_color = resolve(params.get("background_color", base.background_color))
    return replace(base, max_width=max(1, max_width), background_color=background_color)


# ------------------------------------------------------------------
# Parsowanie #content
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


def _build_sections(lines: list[str], tokens: DesignTokens) -> list[Section]:
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

        if line == "@@row":
            if current_section_children is None:
                continue
            flush_row()
            current_row = Row(
                max_width=tokens.row.max_width,
                background_color=tokens.row.background_color,
                children=[],
            )
            continue

        if line == "@@column":
            if current_row is None:
                continue
            flush_column()
            current_column = Column(children=[])
            continue

        if current_section_children is None:
            continue

        component = _parse_component(line, tokens)
        if component is None:
            continue

        # Wstawiaj do najgłębszego otwartego kontenera
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
        return Button(
            label=value,
            typography=tokens.button_text,
            style=tokens.button,
        )

    return None
