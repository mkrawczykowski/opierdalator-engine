@dataclass
class TypographyToken:
    font_path: str
    font_size: int
    line_height: int
    font_weight: int
    letter_spacing: int
    color: str


@dataclass
class ButtonToken:
    padding_x: int
    padding_y: int
    radius: int
    border_width: int
    background: str
    border_color: str
    text_color: str


@dataclass
class SpacingToken:
    container_width: int
    section_padding_top: int
    section_padding_bottom: int
    margin: int



@dataclass
class ColorToken:
    background: str
    surface: str
    primary: str
    secondary: str
    accent: str
    text: str


@dataclass
class DesignTokens:
    heading: TypographyToken
    body: TypographyToken
    button_text: TypographyToken
    spacing: SpacingToken
    button: ButtonToken
    colors: ColorToken


def default_tokens() -> DesignTokens:
    return DesignTokens(
        heading=TypographyToken(
            font_path="assets/fonts/Inter-Bold.ttf",
            font_size=56,
            line_height=64,
            font_weight=700,
            letter_spacing=0,
            color="#1F2937",
        ),
        body=TypographyToken(
            font_path="assets/fonts/Inter-Regular.ttf",
            font_size=20,
            line_height=30,
            font_weight=400,
            letter_spacing=0,
            color="#374151",
        ),
        button_text=TypographyToken(
            font_path="assets/fonts/Inter-SemiBold.ttf",
            font_size=18,
            line_height=24,
            font_weight=600,
            letter_spacing=0,
            color="#FFFFFF",
        ),
        spacing=SpacingToken(
            container_width=900,
            section_padding_top=96,
            section_padding_bottom=96,
            margin=32,
        ),
        button=ButtonToken(
            padding_x=32,
            padding_y=18,
            radius=12,
            border_width=0,
            background="#3B82F6",
            border_color="#3B82F6",
            text_color="#FFFFFF",
        ),
        colors=ColorToken(
            background="#FFFFFF",
            surface="#F8FAFC",
            primary="#2563EB",
            secondary="#64748B",
            accent="#14B8A6",
            text="#1F2937",
        ),
    )