from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from oe.palette import PaletteGenerator

from .sections import (
    draw_title,
    draw_palette,
    draw_typography,
    draw_button,
    draw_card,
    draw_hero,
    draw_variation,
)


class PNGRenderer:

    WIDTH = 1000
    HEIGHT = 900

    def render(
        self,
        dna,
        variation,
        filename,
    ):

        palette = PaletteGenerator().generate(
            variation
        )

        image = Image.new(
            "RGB",
            (self.WIDTH, self.HEIGHT),
            palette["background"]
        )

        draw = ImageDraw.Draw(image)

        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()

        draw_title(
            draw,
            title_font,
        )

        draw_palette(
            draw,
            body_font,
            palette,
        )

        draw_typography(
            draw,
            title_font,
            body_font,
        )

        draw_button(
            draw,
            body_font,
        )

        draw_card(
            draw,
            body_font,
        )

        draw_hero(
            draw,
            title_font,
            body_font,
        )

        draw_variation(
            draw,
            body_font,
            variation,
        )

        image.save(
            filename
        )