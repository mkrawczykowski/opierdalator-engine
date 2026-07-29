from PIL import Image, ImageDraw

from oe.design.tokens import DesignTokens
from oe.renderer.components.section import Section
from oe.renderer.layout.vertical_layout import VerticalLayout
from oe.renderer.layout.node_painter import NodePainter


class LayoutRenderer:
    """
    Renderer oparty na DesignTokens i silniku layoutu.

    Pipeline:
        list[Section]
            ↓  VerticalLayout
        list[LayoutNode]
            ↓  NodePainter
        PNG

    LayoutRenderer nie zna pojęć takich jak boldness czy elegance.
    Operuje wyłącznie na DesignTokens i drzewie komponentów.
    """

    def render(
        self,
        sections: list[Section],
        tokens: DesignTokens,
        filename: str,
    ) -> None:
        canvas_width = tokens.spacing.container_width + tokens.spacing.margin * 2

        layout = VerticalLayout(
            spacing=tokens.spacing,
            canvas_width=canvas_width,
        )

        nodes = layout.build(sections)

        canvas_height = sum(node.height for node in nodes)
        canvas_height = max(canvas_height, 100)

        image = Image.new(
            "RGB",
            (canvas_width, canvas_height),
            tokens.colors.background,
        )

        draw = ImageDraw.Draw(image)

        painter = NodePainter()

        for node in nodes:
            painter.paint(draw, node)

        image.save(filename)
