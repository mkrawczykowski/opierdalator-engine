from oe import VERSION
from oe.theme import ThemeDNA
from oe.variation import VariationEngine
from oe.renderer import PNGRenderer


def main():

    dna = ThemeDNA(

        softness=(0.80, 0.10),
        contrast=(0.30, 0.08),
        rhythm=(0.70, 0.12),
        geometry=(0.40, 0.15),
        elegance=(0.75, 0.10),

    )

    engine = VariationEngine(seed=42)

    renderer = PNGRenderer()

    print()
    print("===================================")
    print("      Opierdalator Engine")
    print("===================================")
    print()
    print(f"Version: {VERSION}")
    print()

    dna.describe()

    print()

    variation = engine.generate(dna)

    renderer.render(
        dna,
        variation,
        "theme_board.png"
    )

    print("Generated: theme_board.png")
    print()


if __name__ == "__main__":
    main()