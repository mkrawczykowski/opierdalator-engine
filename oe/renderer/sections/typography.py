def draw_typography(
    draw,
    title_font,
    body_font,
):

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
        (
            40,
            330
        ),
        "Body text example. This is placeholder content.",
        fill="#555555",
        font=body_font
    )