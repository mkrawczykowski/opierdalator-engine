def draw_button(draw, body_font):

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