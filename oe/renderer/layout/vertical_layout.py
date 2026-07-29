from oe.renderer.components.component import Component
from oe.renderer.components.section import Section
from oe.renderer.components.text import Text
from oe.renderer.components.heading_1 import Heading1
from oe.renderer.components.button import Button
from oe.design.tokens import SpacingToken

from .layout_node import LayoutNode


class VerticalLayout:
    """
    Zamienia deklaratywne drzewo komponentów na drzewo LayoutNode.

    Układ jest całkowicie pionowy: każdy komponent
    umieszczany jest bezpośrednio pod poprzednim.

    VerticalLayout nie rysuje nic.
    Zwraca wyłącznie strukturę danych.
    """

    def __init__(self, spacing: SpacingToken, canvas_width: int):
        self._spacing = spacing
        self._canvas_width = canvas_width

    def build(self, sections: list[Section]) -> list[LayoutNode]:
        """
        Wejście:  lista Section (drzewo komponentów)
        Wyjście:  lista LayoutNode gotowa do rysowania
        """
        nodes: list[LayoutNode] = []
        cursor_y = 0

        for section in sections:
            node = self._build_section(section, cursor_y)
            nodes.append(node)
            cursor_y += node.height

        return nodes

    # ------------------------------------------------------------------

    def _build_section(self, section: Section, y: int) -> LayoutNode:
        pad_top = self._spacing.section_padding_top
        pad_bottom = self._spacing.section_padding_bottom
        margin = self._spacing.margin

        # Oblicz dzieci wewnątrz sekcji zaczynając od pad_top
        children: list[LayoutNode] = []
        inner_y = y + pad_top

        for child in section.children:
            child_node = self._build_child(child, inner_y, margin)
            children.append(child_node)
            inner_y += child_node.height + margin

        section_height = (inner_y - y) + pad_bottom

        return LayoutNode(
            component=section,
            x=0,
            y=y,
            width=self._canvas_width,
            height=section_height,
            children=children,
        )

    def _build_child(
        self,
        component: Component,
        y: int,
        margin: int,
    ) -> LayoutNode:
        margin_left = self._spacing.margin
        inner_width = self._spacing.container_width

        if isinstance(component, Text):
            height = component.token.line_height
            return LayoutNode(
                component=component,
                x=margin_left,
                y=y,
                width=inner_width,
                height=height,
            )

        if isinstance(component, Heading1):
            height = component.token.line_height
            return LayoutNode(
                component=component,
                x=margin_left,
                y=y,
                width=inner_width,
                height=height,
            )

        if isinstance(component, Button):
            height = (
                component.typography.line_height
                + component.style.padding_y * 2
            )
            return LayoutNode(
                component=component,
                x=margin_left,
                y=y,
                width=inner_width,
                height=height,
            )

        # Komponent nieznany — rezerwujemy minimalną przestrzeń
        return LayoutNode(
            component=component,
            x=margin_left,
            y=y,
            width=inner_width,
            height=32,
        )
