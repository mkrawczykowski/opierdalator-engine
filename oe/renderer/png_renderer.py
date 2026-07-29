from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class PNGRenderer:

    WIDTH = 900
    HEIGHT = 700

    def render(self, dna, variation, filename):

        image = Image.new(
            "RGB",
            (self.WIDTH, self.HEIGHT),
            "#f7f7f5"
        )

        draw = ImageDraw.Draw(image)

        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()

        draw.text(
            (40, 30),
            "Opierdalator Engine\nTheme Board",
            fill="black",
            font=title_font
        )

        y = 120

        labels = [
            ("Softness", variation["softness"]),
            ("Contrast", variation["contrast"]),
            ("Rhythm", variation["rhythm"]),
            ("Geometry", variation["geometry"]),
            ("Elegance", variation["elegance"]),
        ]

        for name, value in labels:

            draw.text(
                (40, y),
                f"{name}",
                fill="black",
                font=body_font
            )

            x1 = 180
            x2 = 650

            draw.line(
                (x1, y + 8, x2, y + 8),
                fill="#bbbbbb",
                width=3
            )

            knob = x1 + (x2 - x1) * value

            draw.ellipse(
                (
                    knob - 8,
                    y,
                    knob + 8,
                    y + 16
                ),
                fill="#4f8a6b"
            )

            draw.text(
                (680, y),
                f"{value:.2f}",
                fill="black",
                font=body_font
            )

            y += 90

        image.save(filename)