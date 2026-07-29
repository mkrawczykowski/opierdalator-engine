from dataclasses import dataclass

from oe.design.tokens import TypographyToken

from .component import Component


@dataclass(slots=True)
class Text(Component):
    text: str
    token: TypographyToken