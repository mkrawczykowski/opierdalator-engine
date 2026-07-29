from dataclasses import dataclass


@dataclass
class ThemeDNA:
    """
    Opisuje estetykę projektu.

    Wszystkie wartości są znormalizowane
    do zakresu 0.0–1.0.

    Nie są to jeszcze konkretne wartości
    renderera, tylko cechy wizualne.
    """

    softness: float
    contrast: float
    rhythm: float
    geometry: float
    elegance: float

    def describe(self):

        print("Theme DNA")
        print("-----------------------")
        print(f"Softness : {self.softness:.2f}")
        print(f"Contrast : {self.contrast:.2f}")
        print(f"Rhythm   : {self.rhythm:.2f}")
        print(f"Geometry : {self.geometry:.2f}")
        print(f"Elegance : {self.elegance:.2f}")