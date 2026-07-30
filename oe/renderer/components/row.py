from dataclasses import dataclass, field

from .component import Component


@dataclass(slots=True)
class Row(Component):
    """
    Kontener treści o ograniczonej szerokości, wycentrowany w sekcji.

    max_width       — maksymalna szerokość contentu w px
    background_color — kolor tła
    col_ratios      — proporcje szerokości kolumn, np. (1, 2) dla 1/3 i 2/3
    col_gap_pct     — odstęp między kolumnami jako % szerokości Row (0.0–100.0)
    """
    max_width: int
    background_color: str
    col_ratios: tuple[int, int] = (1, 1)
    col_gap_pct: float = 0.0
    children: list[Component] = field(default_factory=list)
