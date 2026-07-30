from PIL import ImageFont

from oe.renderer.components.component import Component
from oe.renderer.components.section import Section
from oe.renderer.components.row import Row
from oe.renderer.components.column import Column
from oe.renderer.components.text import Text
from oe.renderer.components.heading_1 import Heading1
from oe.renderer.components.button import Button
from oe.design.tokens import SpacingToken

from .layout_node import LayoutNode
from .text_wrapper import TextWrapper


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
        self._wrapper = TextWrapper()

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
                child_node = self._build_leaf(child, inner_y, x=margin,
                                              available_width=self._canvas_width - margin * 2)
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
        """Row wycentrowany poziomo; szerokość = min(max_width, canvas_width).

        Kolumny układane obok siebie zgodnie z col_ratios.
        Odstęp między kolumnami = row_width * col_gap_pct / 100.
        Pozostała szerokość dzielona proporcjonalnie wg col_ratios.
        Wysokość Row = max(height_col_1, height_col_2).
        """
        row_width = min(row.max_width, self._canvas_width)
        row_x     = (self._canvas_width - row_width) // 2

        columns = [c for c in row.children if isinstance(c, Column)]
        non_columns = [c for c in row.children if not isinstance(c, Column)]

        col_widths = self._calc_column_widths(row_width, row.col_ratios, row.col_gap_pct, len(columns))
        gap_px = int(row_width * row.col_gap_pct / 100.0)

        col_nodes: list[LayoutNode] = []
        col_x = row_x
        for i, column in enumerate(columns):
            w = col_widths[i] if i < len(col_widths) else col_widths[-1]
            col_node = self._build_column(column, y, col_x, w)
            col_nodes.append(col_node)
            col_x += w + gap_px

        # Liście bezpośrednio w Row (bez Column) — układane pionowo pod kolumnami
        margin = self._spacing.margin
        leaf_nodes: list[LayoutNode] = []
        inner_y = y
        for child in non_columns:
            leaf_node = self._build_leaf(child, inner_y, x=row_x, available_width=row_width)
            leaf_nodes.append(leaf_node)
            inner_y += leaf_node.height + margin

        row_height = max((n.height for n in col_nodes), default=0)
        if leaf_nodes:
            row_height = max(row_height, inner_y - y - margin)

        return LayoutNode(
            component=row,
            x=row_x,
            y=y,
            width=row_width,
            height=row_height,
            children=col_nodes + leaf_nodes,
        )

    @staticmethod
    def _calc_column_widths(
        row_width: int,
        col_ratios: tuple[int, int],
        col_gap_pct: float,
        col_count: int,
    ) -> list[int]:
        """
        Oblicza szerokości kolumn w px.

        Algorytm:
        1. gap_px = row_width * col_gap_pct / 100  (zaokrąglony w dół)
        2. available = row_width - gap_px * (col_count - 1)
        3. każda kolumna = available * ratio / sum_ratios  (zaokrąglone w dół)
        4. ostatnia kolumna dostaje resztę pikseli
        """
        if col_count == 0:
            return []

        gap_px    = int(row_width * col_gap_pct / 100.0)
        gaps_total = gap_px * max(col_count - 1, 0)
        available  = max(row_width - gaps_total, 0)

        ratios = list(col_ratios[:col_count])
        while len(ratios) < col_count:
            ratios.append(1)

        total_ratio = sum(ratios)
        widths = [int(available * r / total_ratio) for r in ratios]

        # Wyrównaj resztę pikseli do ostatniej kolumny
        widths[-1] = available - sum(widths[:-1])

        return widths

    def _build_column(self, column: Column, y: int, x: int, width: int) -> LayoutNode:
        """Column zajmuje 100% szerokości rodzica Row."""
        margin = self._spacing.margin

        children: list[LayoutNode] = []
        inner_y = y

        for child in column.children:
            child_node = self._build_leaf(child, inner_y, x=x, available_width=width)
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

    def _build_leaf(
        self,
        component: Component,
        y: int,
        x: int,
        available_width: int,
    ) -> LayoutNode:
        """
        Buduje LayoutNode dla komponentu liścia.

        available_width to rzeczywista szerokość kontenera (Column / Row / Section),
        używana do zawijania tekstu i obliczania wysokości.
        """
        if isinstance(component, (Text, Heading1)):
            token = component.token
            font  = self._load_font(token.font_path, token.font_size)
            lines = self._wrapper.wrap(component.text, font, available_width)
            height = self._wrapper.total_height(len(lines), token.line_height)
            return LayoutNode(
                component=component,
                x=x,
                y=y,
                width=available_width,
                height=height,
            )

        if isinstance(component, Button):
            height = component.typography.font_size + component.style.padding_y * 2
            return LayoutNode(
                component=component,
                x=x,
                y=y,
                width=available_width,
                height=height,
            )

        # Komponent nieznany — rezerwujemy minimalną przestrzeń
        return LayoutNode(
            component=component,
            x=x,
            y=y,
            width=available_width,
            height=32,
        )

    # ------------------------------------------------------------------

    _FALLBACK_FONTS = [
        "C:/Windows/Fonts/DejaVuSans.ttf",
        "C:/Windows/Fonts/NotoSans-Regular.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]

    def _load_font(self, font_path: str, font_size: int) -> ImageFont.FreeTypeFont:
        for path in [font_path] + self._FALLBACK_FONTS:
            try:
                return ImageFont.truetype(path, font_size)
            except (OSError, IOError):
                continue
        return ImageFont.load_default()
