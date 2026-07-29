from dataclasses import dataclass

from oe.design.tokens import TypographyToken

from .component import Component


@dataclass(slots=True)
class Heading1(Component):
    text: str
    token: TypographyToken
