from dataclasses import dataclass, field

from .component import Component


@dataclass(slots=True)
class Section(Component):
    children: list[Component] = field(default_factory=list)