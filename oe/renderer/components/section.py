from dataclasses import dataclass, field

from .component import Component


@dataclass(slots=True)
class Section(Component):
    background_color: str = "#FFFFFF"
    children: list[Component] = field(default_factory=list)