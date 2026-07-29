from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from oe.renderer.components.component import Component


@dataclass
class LayoutNode:
    """
    Przechowuje pozycję i wymiary jednego komponentu
    po obliczeniu layoutu.

    LayoutNode nie zawiera logiki layoutu.
    Jest wyłącznie kontenerem danych przekazywanych do renderera.
    """

    component: "Component"
    x: int
    y: int
    width: int
    height: int
    children: list[LayoutNode] = field(default_factory=list)
