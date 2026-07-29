from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class PNGRenderer:

    WIDTH = 1000
    HEIGHT = 900
    MARGIN = 40

    def render(self, dna, variation, filename):

        image = Image.new(
            "RGB",
            (self.WIDTH, self.HEIGHT),
            "#F5F5F3"
        )

        draw = ImageDraw.Draw(image)

        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()

        # -------------------------------------------------
        # Title
        # -------------------------------------------------

        draw.text(
            (40, 30),
            "Opierdalator Engine\nTheme Board",
            fill="black",
            font=title_font
        )

        # -------------------------------------------------
        # Color Palette
        # -------------------------------------------------

        draw.text(
            (40, 100),
            "Color Palette",
            fill="black",
            font=body_font
        )

        colors = [
            "#496A81",
            "#8CAFB8",
            "#D9E4DD",
            "#FFFFFF",
            "#2D3436"
        ]

        x = 40

        for color in colors:

            draw.rounded_rectangle(
                (x, 130, x + 90, 220),
                radius=12,
                fill=color
            )

            x += 110

        # -------------------------------------------------
        # Typography
        # -------------------------------------------------

        draw.text(
            (40, 260),
            "Typography",
            fill="black",
            font=body_font
        )

        draw.text(
            (40, 300),
            "Heading Example",
            fill="black",
            font=title_font
        )

        draw.text(
            (40, 330),
            "Body text example. This is placeholder content.",
            fill="#555555",
            font=body_font
        )

        # -------------------------------------------------
        # Button
        # -------------------------------------------------

        draw.text(
            (40, 390),
            "Button",
            fill="black",
            font=body_font
        )

        draw.rounded_rectangle(
            (40, 420, 220, 470),
            radius=12,
            fill="#496A81"
        )

        draw.text(
            (90, 438),
            "Book Session",
            fill="white",
            font=body_font
        )

        # -------------------------------------------------
        # Card
        # -------------------------------------------------

        draw.text(
            (300, 390),
            "Card",
            fill="black",
            font=body_font
        )

        draw.rounded_rectangle(
            (300, 420, 620, 620),
            radius=14,
            fill="white",
            outline="#DDDDDD"
        )

        draw.text(
            (330, 450),
            "Card title",
            fill="black",
            font=body_font
        )

        draw.text(
            (330, 490),
            "Lorem ipsum dolor sit amet,\nconsectetur adipiscing elit.",
            fill="#666666",
            font=body_font
        )

        # -------------------------------------------------
        # Hero Preview
        # -------------------------------------------------

        draw.text(
            (40, 660),
            "Hero Preview",
            fill="black",
            font=body_font
        )

        draw.rounded_rectangle(
            (40, 690, 920, 840),
            radius=16,
            fill="#E9EFEA"
        )

        draw.text(
            (80, 720),
            "Find calm.\nFind clarity.",
            fill="#2D3436",
            font=title_font
        )

        draw.text(
            (80, 770),
            "Example hero section for visual testing.",
            fill="#555555",
            font=body_font
        )

        # -------------------------------------------------
        # Variation Values
        # -------------------------------------------------

        y = 100

        draw.text(
            (760, 100),
            "Variation",
            fill="black",
            font=body_font
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

            draw.text(
                (760, y),
                f"{name}: {value:.2f}",
                fill="black",
                font=body_font
            )

            y += 35

        image.save(filename)