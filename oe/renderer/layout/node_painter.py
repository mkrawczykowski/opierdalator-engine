from PIL import ImageDraw, ImageFont

from oe.renderer.components.text import Text
from oe.renderer.components.heading_1 import Heading1
from oe.renderer.components.button import Button
from oe.renderer.components.section import Section

from .layout_node import LayoutNode


class NodePainter:
    """
    Rysuje jedno drzewo LayoutNode na kontekście ImageDraw.

    NodePainter nie zna pojęć takich jak boldness czy elegance.
    Operuje wyłącznie na danych zawartych w LayoutNode
    i DesignTokens przypisanych do komponentów.
    """

    def paint(self, draw: ImageDraw.ImageDraw, node: LayoutNode) -> None:
        """Rysuje node i rekurencyjnie wszystkich jego potomków."""
        self._paint_node(draw, node)
        for child in node.children:
            self.paint(draw, child)

    # ------------------------------------------------------------------

    def _paint_node(
        self,
        draw: ImageDraw.ImageDraw,
        node: LayoutNode,
    ) -> None:
        component = node.component

        if isinstance(component, Section):
            self._paint_section(draw, node)
        elif isinstance(component, Heading1):
            self._paint_text(draw, node)
        elif isinstance(component, Text):
            self._paint_text(draw, node)
        elif isinstance(component, Button):
            self._paint_button(draw, node)

    # ------------------------------------------------------------------

    def _paint_section(
        self,
        draw: ImageDraw.ImageDraw,
        node: LayoutNode,
    ) -> None:
        draw.rectangle(
            (node.x, node.y, node.x + node.width, node.y + node.height),
            fill=None,
            outline=None,
        )

    def _paint_text(
        self,
        draw: ImageDraw.ImageDraw,
        node: LayoutNode,
    ) -> None:
        component: Text = node.component  # type: ignore[assignment]
        token = component.token

        font = self._load_font(token.font_path, token.font_size)

        draw.text(
            (node.x, node.y),
            component.text,
            fill=token.color,
            font=font,
        )

    def _paint_button(
        self,
        draw: ImageDraw.ImageDraw,
        node: LayoutNode,
    ) -> None:
        component: Button = node.component  # type: ignore[assignment]
        style = component.style
        typography = component.typography

        btn_width = typography.font_size * len(component.label) // 2 + style.padding_x * 2
        btn_height = node.height

        x0 = node.x
        y0 = node.y
        x1 = x0 + btn_width
        y1 = y0 + btn_height

        draw.rounded_rectangle(
            (x0, y0, x1, y1),
            radius=style.radius,
            fill=style.background,
            outline=style.border_color if style.border_width > 0 else None,
            width=style.border_width,
        )

        font = self._load_font(typography.font_path, typography.font_size)

        text_x = x0 + style.padding_x
        text_y = y0 + style.padding_y

        draw.text(
            (text_x, text_y),
            component.label,
            fill=style.text_color,
            font=font,
        )

    # ------------------------------------------------------------------

    # Systemowe fonty z pełnym wsparciem Unicode (w tym polskie znaki),
    # używane gdy projektowe pliki TTF nie są dostępne.
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
        # Ostateczny fallback — bitmapowy, bez polskich znaków.
        # Nie powinien być osiągany na Windowsie z DejaVu w systemie.
        return ImageFont.load_default()
