from dataclasses import dataclass, field

from .component import Component


@dataclass(slots=True)
class Column(Component):
    """
    Kontener pionowy, dziecko Row.

    Szerokość obliczana przez VerticalLayout na podstawie col_ratios z Row.
    background_color — kolor tła; None oznacza transparentny.
    """
    background_color: str | None = None
    children: list[Component] = field(default_factory=list)
