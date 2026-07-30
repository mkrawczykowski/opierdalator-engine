from oe.renderer.components.component import Component
from oe.renderer.components.section import Section
from oe.renderer.components.row import Row
from oe.renderer.components.column import Column
from oe.renderer.components.text import Text
from oe.renderer.components.heading_1 import Heading1
from oe.renderer.components.button import Button
from oe.design.tokens import SpacingToken

from .layout_node import LayoutNode


class VerticalLayout:
    """
    Zamienia deklaratywne drzewo komponentów na drzewo LayoutNode.

    Hierarchia:
        Section
            Row         (wycentrowany, max_width)
                Column  (100% szerokości Row)
                    Text / Heading1 / Button
            Text / Heading1 / Button  (bezpośrednio w Section)

    VerticalLayout nie rysuje nic — zwraca wyłącznie strukturę danych.
    """

    def __init__(self, spacing: SpacingToken, canvas_width: int):
        self._spacing = spacing
        self._canvas_width = canvas_width

    def build(self, sections: list[Section]) -> list[LayoutNode]:
        nodes: list[LayoutNode] = []
        cursor_y = 0
        for section in sections:
            node = self._build_section(section, cursor_y)
            nodes.append(node)
            cursor_y += node.height
        return nodes

    # ------------------------------------------------------------------

    def _build_section(self, section: Section, y: int) -> LayoutNode:
        pad_top    = self._spacing.section_padding_top
        pad_bottom = self._spacing.section_padding_bottom
        margin     = self._spacing.margin

        children: list[LayoutNode] = []
        inner_y = y + pad_top

        for child in section.children:
            if isinstance(child, Row):
                child_node = self._build_row(child, inner_y)
            else:
                child_node = self._build_leaf(child, inner_y, x=margin)
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

    def _build_row(self, row: Row, y: int) -> LayoutNode:
        """Row wycentrowany poziomo; szerokość = min(max_width, canvas_width)."""
        margin    = self._spacing.margin
        row_width = min(row.max_width, self._canvas_width)
        row_x     = (self._canvas_width - row_width) // 2

        children: list[LayoutNode] = []
        inner_y = y

        for child in row.children:
            if isinstance(child, Column):
                child_node = self._build_column(child, inner_y, row_x, row_width)
            else:
                child_node = self._build_leaf(child, inner_y, x=row_x)
            children.append(child_node)
            inner_y += child_node.height + margin

        row_height = max(inner_y - y - margin, 0) if children else 0

        return LayoutNode(
            component=row,
            x=row_x,
            y=y,
            width=row_width,
            height=row_height,
            children=children,
        )

    def _build_column(
        self,
        column: Column,
        y: int,
        x: int,
        width: int,
    ) -> LayoutNode:
        """Column zajmuje 100% szerokości rodzica Row."""
        margin = self._spacing.margin

        children: list[LayoutNode] = []
        inner_y = y

        for child in column.children:
            child_node = self._build_leaf(child, inner_y, x=x)
            children.append(child_node)
            inner_y += child_node.height + margin

        col_height = max(inner_y - y - margin, 0) if children else 0

        return LayoutNode(
            component=column,
            x=x,
            y=y,
            width=width,
            height=col_height,
            children=children,
        )

    def _build_leaf(self, component: Component, y: int, x: int) -> LayoutNode:
        """Buduje LayoutNode dla komponentu liścia (Text, Heading1, Button)."""
        if isinstance(component, Text):
            return LayoutNode(
                component=component,
                x=x,
                y=y,
                width=self._spacing.container_width,
                height=component.token.line_height,
            )

        if isinstance(component, Heading1):
            return LayoutNode(
                component=component,
                x=x,
                y=y,
                width=self._spacing.container_width,
                height=component.token.line_height,
            )

        if isinstance(component, Button):
            height = component.typography.font_size + component.style.padding_y * 2
            return LayoutNode(
                component=component,
                x=x,
                y=y,
                width=self._spacing.container_width,
                height=height,
            )

        # Komponent nieznany — rezerwujemy minimalną przestrzeń
        return LayoutNode(
            component=component,
            x=x,
            y=y,
            width=self._spacing.container_width,
            height=32,
        )
