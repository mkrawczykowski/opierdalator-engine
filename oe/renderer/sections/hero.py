def draw_hero(
    draw,
    title_font,
    body_font,
):

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