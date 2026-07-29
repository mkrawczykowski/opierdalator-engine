def draw_palette(draw, body_font):

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