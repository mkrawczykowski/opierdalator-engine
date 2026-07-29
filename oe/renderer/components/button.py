from dataclasses import dataclass

from oe.design.tokens import ButtonToken, TypographyToken

from .component import Component


@dataclass(slots=True)
class Button(Component):
    label: str
    typography: TypographyToken
    style: ButtonToken