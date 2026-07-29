"""
Parser plików .md dla Opierdalator Engine.

Obsługiwane sekcje:
    #color_palette  — zmienne kolorów ($nazwa: #hex)
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

import pathlib
from dataclasses import replace

from oe.design.tokens import DesignTokens, ButtonToken
from oe.renderer.components import Section, Text, Heading1, Button
from oe.renderer.components.component import Component


def parse(md_path: pathlib.Path, tokens: DesignTokens) -> list[Section]:
    """
    Wejście:  ścieżka do pliku .md, DesignTokens (wartości domyślne)
    Wyjście:  lista Section gotowa do przekazania do LayoutRenderer

    Tokeny z pliku MD nadpisują wartości domyślne tam, gdzie
    plik MD definiuje odpowiednie parametry.
    """
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    colors = _parse_color_palette(lines)
    tokens = _apply_components(lines, tokens, colors)
    content_lines = _extract_section_lines(lines, "#content")
    return _build_sections(content_lines, tokens)


def parse_tokens(md_path: pathlib.Path, tokens: DesignTokens) -> DesignTokens:
    """
    Wyjmuje z pliku MD tokeny (kolory, parametry komponentów)
    i zwraca zaktualizowane DesignTokens — bez budowania sekcji.

    Używane gdy caller chce zmodyfikować tokeny (np. przez TokenVariator)
    przed ostatecznym zbudowaniem drzewa komponentów.
    """
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    colors = _parse_color_palette(lines)
    return _apply_components(lines, tokens, colors)


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

    Aktualnie obsługuje: button (background_color, padding_vertical,
    padding_horizontal, border).
    """
    component_lines = _extract_section_lines(lines, "#components")
    button_params = _parse_component_block(component_lines, "button")

    if not button_params:
        return tokens

    new_button = _build_button_token(tokens.button, button_params, colors)
    return replace(tokens, button=new_button)


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
    """Tworzy ButtonToken przez nadpisanie wartości bazowych parametrami z pliku."""

    def resolve(value: str) -> str:
        """Zamienia $zmienna na hex z palety kolorów."""
        if value.startswith("$"):
            return colors.get(value[1:], value)
        return value

    def to_int(value: str, default: int) -> int:
        try:
            return int(value)
        except ValueError:
            return default

    background = resolve(params.get("background_color", base.background))
    padding_y = to_int(params.get("padding_vertical", ""), base.padding_y)
    padding_x = to_int(params.get("padding_horizontal", ""), base.padding_x)
    border_width = to_int(params.get("border", ""), base.border_width)

    return replace(
        base,
        background=background,
        border_color=background,
        padding_x=padding_x,
        padding_y=padding_y,
        border_width=border_width,
    )


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
    current_children: list[Component] | None = None

    for line in lines:
        if not line:
            continue

        if line == "@@section":
            if current_children is not None:
                sections.append(Section(children=current_children))
            current_children = []
            continue

        if current_children is None:
            continue

        component = _parse_component(line, tokens)
        if component is not None:
            current_children.append(component)

    if current_children is not None:
        sections.append(Section(children=current_children))

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
