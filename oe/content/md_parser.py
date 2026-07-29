"""
Parser sekcji #content z plików .md.

Format:
    #content
    @@section
    @@heading_1: Treść nagłówka
    @@text: Treść akapitu
    @@button: Etykieta przycisku

    @@section
    @@heading_1: ...
    ...

Zasady:
- Parser czyta wyłącznie zawartość sekcji #content.
- Każda linia zaczynająca się od @@ to deklaracja komponentu.
- Pusta linia jest ignorowana.
- Linie poza sekcją #content są ignorowane.
- @@section otwiera nową sekcję; następne komponenty trafiają do niej.
- Komponenty przed pierwszym @@section są ignorowane.
"""

import pathlib

from oe.design.tokens import DesignTokens
from oe.renderer.components import Section, Text, Heading1, Button
from oe.renderer.components.component import Component


def parse(md_path: pathlib.Path, tokens: DesignTokens) -> list[Section]:
    """
    Wejście:  ścieżka do pliku .md, DesignTokens
    Wyjście:  lista Section gotowa do przekazania do LayoutRenderer
    """
    text = md_path.read_text(encoding="utf-8")
    content_lines = _extract_content_lines(text)
    return _build_sections(content_lines, tokens)


# ------------------------------------------------------------------


def _extract_content_lines(text: str) -> list[str]:
    """Zwraca linie należące do sekcji #content."""
    lines = text.splitlines()
    inside = False
    result: list[str] = []

    for line in lines:
        stripped = line.strip()

        if stripped == "#content":
            inside = True
            continue

        # Nowa sekcja najwyższego poziomu kończy #content
        if inside and stripped.startswith("#") and not stripped.startswith("##") and stripped != "#content":
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
            # Komponent przed pierwszym @@section — ignoruj
            continue

        component = _parse_component(line, tokens)
        if component is not None:
            current_children.append(component)

    # Domknij ostatnią sekcję
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
