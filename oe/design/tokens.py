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