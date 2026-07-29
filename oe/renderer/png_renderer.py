from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from .sections import (
    draw_title,
    draw_palette,
    draw_typography,
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

        self.image = Image.new(
            "RGB",
            (
                self.WIDTH,
                self.HEIGHT,
            ),
            "#F5F5F3"
        )

        self.draw = ImageDraw.Draw(
            self.image
        )

        self.title_font = ImageFont.load_default()
        self.body_font = ImageFont.load_default()

        draw_title(
            self.draw,
            self.title_font,
        )

        draw_palette(
            self.draw,
            self.body_font,
        )

        draw_typography(
            self.draw,
            self.title_font,
            self.body_font,
        )

        #
        # Te sekcje przeniesiemy
        # w następnym commicie.
        #

        self._draw_button()
        self._draw_card()
        self._draw_hero()
        self._draw_variation_values(
            variation
        )

        self.image.save(
            filename
        )

    # -------------------------------------------------

    def _draw_button(self):

        self.draw.text(
            (40, 390),
            "Button",
            fill="black",
            font=self.body_font
        )

        self.draw.rounded_rectangle(
            (40, 420, 220, 470),
            radius=12,
            fill="#496A81"
        )

        self.draw.text(
            (90, 438),
            "Book Session",
            fill="white",
            font=self.body_font
        )

    # -------------------------------------------------

    def _draw_card(self):

        self.draw.text(
            (300, 390),
            "Card",
            fill="black",
            font=self.body_font
        )

        self.draw.rounded_rectangle(
            (300, 420, 620, 620),
            radius=14,
            fill="white",
            outline="#DDDDDD"
        )

        self.draw.text(
            (330, 450),
            "Card title",
            fill="black",
            font=self.body_font
        )

        self.draw.text(
            (
                330,
                490
            ),
            "Lorem ipsum dolor sit amet,\nconsectetur adipiscing elit.",
            fill="#666666",
            font=self.body_font
        )

    # -------------------------------------------------

    def _draw_hero(self):

        self.draw.text(
            (40, 660),
            "Hero Preview",
            fill="black",
            font=self.body_font
        )

        self.draw.rounded_rectangle(
            (40, 690, 920, 840),
            radius=16,
            fill="#E9EFEA"
        )

        self.draw.text(
            (
                80,
                720
            ),
            "Find calm.\nFind clarity.",
            fill="#2D3436",
            font=self.title_font
        )

        self.draw.text(
            (
                80,
                770
            ),
            "Example hero section for visual testing.",
            fill="#555555",
            font=self.body_font
        )

    # -------------------------------------------------

    def _draw_variation_values(
        self,
        variation,
    ):

        self.draw.text(
            (
                760,
                100
            ),
            "Variation",
            fill="black",
            font=self.body_font
        )

        labels = [
            ("Softness", variation["softness"]),
            ("Contrast", variation["contrast"]),
            ("Rhythm", variation["rhythm"]),
            ("Geometry", variation["geometry"]),
            ("Elegance", variation["elegance"]),
        ]

        y = 130

        for name, value in labels:

            self.draw.text(
                (
                    760,
                    y
                ),
                f"{name}: {value:.2f}",
                fill="black",
                font=self.body_font
            )

            y += 35