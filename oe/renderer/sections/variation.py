def draw_variation(
    draw,
    body_font,
    variation,
):

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