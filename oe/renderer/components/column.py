from dataclasses import dataclass, field

from .component import Component


@dataclass(slots=True)
class Column(Component):
    """
    Kontener pionowy, dziecko Row.

    Na razie zajmuje 100% szerokości rodzica Row.
    Jest transparentny — nie rysuje tła ani obramowania.
    Służy wyłącznie do grupowania i pozycjonowania dzieci.
    """
    children: list[Component] = field(default_factory=list)
