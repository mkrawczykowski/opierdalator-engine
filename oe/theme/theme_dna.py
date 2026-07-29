from dataclasses import dataclass


@dataclass
class ThemeDNA:
    """
    Opisuje estetykę marki.

    Każda cecha jest opisana przez:

    - wartość docelową
    - maksymalne odchylenie

    Variation Engine będzie losował
    konkretną wartość z tego zakresu.
    """

    softness: tuple[float, float]
    contrast: tuple[float, float]
    rhythm: tuple[float, float]
    geometry: tuple[float, float]
    elegance: tuple[float, float]

    def describe(self):

        print("Theme DNA")
        print("-------------------------")

        self._print("Softness", self.softness)
        self._print("Contrast", self.contrast)
        self._print("Rhythm", self.rhythm)
        self._print("Geometry", self.geometry)
        self._print("Elegance", self.elegance)

    def _print(self, name, value):

        target, variation = value

        print(
            f"{name:10} target={target:.2f} variation=±{variation:.2f}"
        )