from dataclasses import dataclass, field

from .component import Component


@dataclass(slots=True)
class Row(Component):
    """
    Kontener treści o ograniczonej szerokości, wycentrowany w sekcji.

    max_width narzuca maksymalną szerokość contentu.
    background_color to kolor tła obszaru Row.
    Dzieci są rysowane wewnątrz tego obszaru.
    """
    max_width: int
    background_color: str
    children: list[Component] = field(default_factory=list)
