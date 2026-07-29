def draw_card(draw, body_font):

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