def draw_palette(
    draw,
    body_font,
    palette,
):

    draw.text(
        (40, 100),
        "Color Palette",
        fill="black",
        font=body_font
    )

    colors = [
        palette["primary"],
        palette["secondary"],
        palette["surface"],
        palette["background"],
        palette["text"],
    ]

    x = 40

    for color in colors:

        draw.rounded_rectangle(
            (
                x,
                130,
                x + 90,
                220
            ),
            radius=12,
            fill=color
        )

        x += 110