from dataclasses import dataclass


@dataclass(slots=True)
class Component:
    """Base class for every declarative renderer component."""
    pass